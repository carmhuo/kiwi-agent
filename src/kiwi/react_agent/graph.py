"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from datetime import UTC, datetime
from typing import Dict, List, Literal, cast, Optional
from functools import lru_cache
import logging

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from kiwi.react_agent.configuration import Configuration
from kiwi.react_agent.state import InputState, State
from kiwi.react_agent.tools import TOOLS, build_tool_system
from kiwi.react_agent.utils import load_chat_model, from_duckdb

from dotenv import load_dotenv

load_dotenv(override=True)  # load environment variables from .env

# Global variables for lazy initialization
_db_instance = None
_llm_instance = None
_tools_instance = None
_graph_instance = None

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_database_connection(database_path: str, read_only: bool = True):
    """Get a cached DuckDB connection to avoid multiple connections.
    
    Args:
        database_path: Path to the DuckDB database file.
        read_only: Whether to open the database in read-only mode.
        
    Returns:
        A DuckDB connection object (cached for subsequent calls).
        
    Raises:
        RuntimeError: If database connection fails.
    """
    try:
        db = from_duckdb(database_path, read_only)
        logger.debug(f"Initialized DuckDB connection: {database_path} (read_only={read_only})")
        return db
    except Exception as e:
        logger.error(f"Failed to connect to DuckDB: {e}")
        raise RuntimeError(f"Failed to connect to DuckDB: {e}") from e

@lru_cache(maxsize=1) 
def get_llm_instance(model: str):
    """Get LLM instance with caching."""
    return load_chat_model(model)

def get_tools(config: Optional[Configuration] = None):
    """Get tools with lazy initialization."""
    global _tools_instance
    
    if _tools_instance is None:
        if config is None:
            config = Configuration.from_context()
        
        db = get_database_connection(config.database_path, config.read_only)
        llm = get_llm_instance(config.model)
        _tools_instance = build_tool_system(db, llm, config)
        
        # Only print database info when tools are first initialized
        print(f"{db.dialect}: {db.get_usable_table_names()}")
    
    return _tools_instance

async def call_model(state: State) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering our "agent".

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    config = Configuration.from_context()

    # Get tools and database connection using lazy initialization
    tools = get_tools(config)
    db = get_database_connection(config.database_path, config.read_only)

    # Initialize the model with tool binding. Change the model or add more tools here.
    model = get_llm_instance(config.model).bind_tools(tools)

    # Format the system prompt. Customize this to change the agent's behavior.
    system_message = config.system_prompt.format(
        dialect=db.dialect,
        top_k=10,
        system_time=datetime.now().isoformat()
    )

    # Get the model's response
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages],
            extra_body={"enable_thinking": False}
        ),
    )

    # Handle the case when it's the last step and the model still wants to use a tool
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, I could not find an answer to your question in the specified number of steps.",
                )
            ]
        }

    # Return the model's response as a list to be added to existing messages
    return {"messages": [response]}


def route_model_output(state: State) -> Literal["__end__", "tools"]:
    """Determine the next node based on the model's output.

    This function checks if the model's last message contains tool calls.

    Args:
        state (State): The current state of the conversation.

    Returns:
        str: The name of the next node to call ("__end__" or "tools").
    """
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in output edges, but got {type(last_message).__name__}"
        )
    # If there is no tool call, then we finish
    if not last_message.tool_calls:
        return "__end__"
    # Otherwise we execute the requested actions
    return "tools"


def create_graph(config: Optional[Configuration] = None):
    """Create and compile the ReAct agent graph with lazy initialization.
    
    Args:
        config: Optional configuration. If None, will use Configuration.from_context()
        
    Returns:
        Compiled LangGraph instance
    """
    if config is None:
        config = Configuration.from_context()
    
    # Get tools using lazy initialization
    tools = get_tools(config)
    
    # Define a new graph
    builder = StateGraph(State, input=InputState, config_schema=Configuration)

    # Define the two nodes we will cycle between
    builder.add_node(call_model)
    builder.add_node("tools", ToolNode(tools))

    # Set the entrypoint as `call_model`
    # This means that this node is the first one called
    builder.add_edge("__start__", "call_model")

    # Add a conditional edge to determine the next step after `call_model`
    builder.add_conditional_edges(
        "call_model",
        # After call_model finishes running, the next node(s) are scheduled
        # based on the output from route_model_output
        route_model_output,
    )

    # Add a normal edge from `tools` to `call_model`
    # This creates a cycle: after using tools, we always return to the model
    builder.add_edge("tools", "call_model")

    # Compile the builder into an executable graph
    return builder.compile(name="ReAct Agent")


def get_graph(config: Optional[Configuration] = None):
    """Get the compiled graph with lazy initialization and caching."""
    global _graph_instance
    
    if _graph_instance is None:
        _graph_instance = create_graph(config)
    
    return _graph_instance


# For backward compatibility, create a lazy graph attribute
class _LazyGraph:
    """Lazy graph loader for backward compatibility."""
    def __init__(self):
        self._graph = None
        self._initialized = False
    
    def __getattr__(self, name):
        # Don't trigger initialization for private attributes or common inspection attributes
        if name.startswith('_') or name in ('__class__', '__dict__', '__module__'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        if self._graph is None:
            self._graph = get_graph()
            self._initialized = True
        return getattr(self._graph, name)
    
    def __call__(self, *args, **kwargs):
        if self._graph is None:
            self._graph = get_graph()
            self._initialized = True
        return self._graph(*args, **kwargs)
    
    def __repr__(self):
        if self._graph is None:
            return f"<{self.__class__.__name__}: Not initialized>"
        return repr(self._graph)

# Create lazy graph instance for backward compatibility
graph = _LazyGraph()


def reset_instances():
    """Reset all cached instances. Useful for testing or configuration changes."""
    global _db_instance, _llm_instance, _tools_instance, _graph_instance
    
    _db_instance = None
    _llm_instance = None
    _tools_instance = None
    _graph_instance = None
    
    # Clear LRU caches
    get_database_connection.cache_clear()
    get_llm_instance.cache_clear()
    
    # Reset lazy graph
    if hasattr(graph, '_graph'):
        graph._graph = None


# Export main functions for external use
__all__ = [
    'get_graph',
    'create_graph', 
    'get_tools',
    'get_database_connection',
    'get_llm_instance',
    'reset_instances',
    'graph'  # For backward compatibility
]
