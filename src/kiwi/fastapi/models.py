# backend/app/models/chat.py
from typing import List, Optional, Any
from pydantic import BaseModel, Field

class MessageItem(BaseModel):
    role: str
    content: str

class AgentConfig(BaseModel):
    """Agent configuration parameters"""
    system_prompt: Optional[str] = Field(
        default=None,
        description="The system prompt to use for the agent's interactions"
    )
    model: Optional[str] = Field(
        default=None,
        description="The language model to use for the agent's main interactions"
    )
    max_search_results: Optional[int] = Field(
        default=None,
        description="The maximum number of search results to return for each search query"
    )
    database_path: Optional[str] = Field(
        default=None,
        description="Filesystem path to the DuckDB database file"
    )
    read_only: Optional[bool] = Field(
        default=None,
        description="Whether to open the database in read-only mode"
    )

class ChatRequest(BaseModel):
    messages: List[MessageItem]
    config: Optional[AgentConfig] = Field(
        default=None,
        description="Configuration parameters for the agent"
    )

# Example, you might want to align this with AIMessage.model_dump() structure
class StreamedChatMessage(BaseModel):
    id: Optional[str] = None
    role: str
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Any]] = None # Or a more specific Pydantic model for tool calls
    # Add other fields if your AIMessage.model_dump_json() includes them