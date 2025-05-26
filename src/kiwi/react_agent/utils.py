"""Utility & helper functions."""
import os

from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    # provider, model = fully_specified_name.split("/", maxsplit=1)
    # llm = ChatOpenAI(
    #     model=os.getenv("MODELSCOPE_MODEL"),
    #     base_url=os.getenv("MODELSCOPE_API_BASE"),
    #     api_key=os.getenv("MODELSCOPE_API_KEY"),  # ModelScope Token
    #     temperature=0
    # )
    assert "OPENAI_API_KEY" in os.environ, "Please provide API Key."
    model = "Qwen/Qwen2.5-32B-Instruct"
    if fully_specified_name:
        model = fully_specified_name
    provide = "openai"
    base_url = os.getenv("OPENAI_API_BASE")
    llm = init_chat_model(model=model, model_provider=provide, 
                        base_url=base_url, temperature=0.7)
    return llm


def from_duckdb(uri: str = ":memory:", read_only=True) -> SQLDatabase:

    """
    Load a DuckDB database connection using SQLAlchemy engine.
    
    Args:
        path: Optional path to DuckDB file. Defaults to enterprise dataset location.
              Use ":memory:" for in-memory database.
    
    Returns:
        SQLDatabase instance configured for DuckDB
        
    Raises:
        RuntimeError: If connection fails
        ValueError: If missing database path

    Examples:
        1. In-memory temporary database: db = from_duckdb(":memory:")
        2. Custom database location: db = from_duckdb("/data/my_db.db")
    """
    try:
        # Use provided path or default location
        db_uri = f"duckdb:///{uri}"  # Correct URI format with 3 slashes
        
        engine = create_engine(
            db_uri,
            connect_args={
                "read_only": read_only  # Ensure read-only access for production safety
            }
        )
        
        # Verify connection
        # with engine.connect() as test_conn:
        #     test_conn.execute("SELECT 1")  # Simple connection test
            
        return SQLDatabase(engine=engine)
    
    except SQLAlchemyError as e:
        raise RuntimeError(
            f"无法连接至DuckDB数据库：{db_uri} (只读模式: {read_only})"
        ) from e