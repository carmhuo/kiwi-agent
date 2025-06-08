"""Utility & helper functions."""
import os
from datetime import datetime
from functools import lru_cache
from urllib.parse import urlparse

from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# Get current date in a readable format
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_current_date():
    return datetime.now().strftime("%B %d, %Y")


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


@lru_cache(maxsize=1)
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


def _duckdb_init_sql() -> str:
    """ Get database init script path from environment"""
    init_sql = None
    init_script_path = os.getenv('DUCKDB_INIT_SCRIPT')

    if init_script_path and os.path.exists(init_script_path):
        try:
            with open(init_script_path, 'r', encoding='utf-8') as f:
                init_sql = f.read()
            print(f"✅ Loaded duckdb initialization script from {init_script_path}")
        except Exception as e:
            print(f"❌ Failed to read init script: {str(e)}")
            # raise RuntimeError(
            #     f"❌ Failed to read init script: {str(e)}"
            # ) from e
    return init_sql


@lru_cache(maxsize=1)
def from_duckdb() -> SQLDatabase:
    """
    Load a DuckDB database connection using SQLAlchemy engine.
    A local DuckDB database can be accessed using the SQLAlchemy URI: duckdb:///path/to/file.db

    
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
        uri = os.environ.get("DUCKDB_PATH", ":memory:")
        read_only = os.environ.get("DUCKDB_READ_ONLY", False)
        memory_limit = os.environ.get("DUCKDB_MEM_LIMIT", '500MB')

        init_script = _duckdb_init_sql()
        path = ":memory:"
        if uri == ":memory:" or uri == "":
            path = ":memory:"
        else:
            print(os.path.exists(uri))
            if os.path.exists(uri):
                path = uri
            elif uri.startswith("md") or uri.startswith("motherduck"):
                path = uri
        # Use provided path or default location
        db_uri = f"duckdb:///{path}"  # Correct URI format with 3 slashes
        engine = create_engine(
            db_uri,
            connect_args={
                "read_only": bool(read_only),  # Ensure read-only access for production safety
                'config': {
                    'memory_limit': memory_limit
                }
            },
            echo=False
        )

        # Verify connection
        # with engine.connect() as test_conn:
        #     test_conn.execute("SELECT 1")  # Simple connection test
        db = SQLDatabase(engine=engine)
        if init_script:
            print(f"init_script: {init_script}")
            db.run(init_script)
        print(f"{db.dialect}: {db.get_usable_table_names()}")
        return db

    except SQLAlchemyError as e:
        raise RuntimeError(
            f"无法连接至DuckDB数据库：{db_uri} (只读模式: {read_only})"
        ) from e

# if __name__ == "__main__":
#     from dotenv import load_dotenv
#
#     load_dotenv()  # load environment variables from .env
#     from_duckdb()
