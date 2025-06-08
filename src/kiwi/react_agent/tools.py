"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""
import json
from typing import Any, Callable, List, Optional, cast, Union, Sequence, Dict
from functools import partial

from langchain_core.tools import tool, BaseTool
from langchain_tavily import TavilySearch
from langchain_community.agent_toolkits import SQLDatabaseToolkit

from kiwi.react_agent.configuration import Configuration
from kiwi.react_agent.utils import load_chat_model, from_duckdb

async def web_search(query: str) -> Optional[dict[str, Any]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    configuration = Configuration.from_runnable_config()
    wrapped = TavilySearch(max_results=configuration.max_search_results)
    return cast(dict[str, Any], await wrapped.ainvoke({"query": query}))


@tool(response_format="content_and_artifact")
def search_proper_nouns(query: str):
    """Use to look up values to filter on. Input is an approximate spelling of the proper noun,
    output is valid proper nouns. Use the noun most similar to the search."""
    retrieved_docs = vector_store.similarity_search(query, k=5)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


@tool
async def upper_text(query: str) -> str:
    """Used to convert text to uppercase. The input is simple text, Output as uppercase text
    """
    return query.upper()

@tool
async def example_selector(query: str) -> Union[str, Sequence[Dict[str, Any]]]:
    """Get some examples of natural language problems and corresponding SQL query.
    Input is a user question, output is a comma-separated list of QUERY-SQL pairs.
    Args:
        query: str type, natural language questions.

    Returns:
        list[dict]: The extracted documents, or an empty list or single document if an error occurred.

    Examples:
        [{'question': 'List all artists.', 'sql': 'SELECT * FROM Artist;'},
         {'question': 'How many employees are there','sql': 'SELECT COUNT(*) FROM "Employee"'},
         {'question': 'How many tracks are there in the album with ID 5?',
          'sql': 'SELECT COUNT(*) FROM Track WHERE AlbumId = 5;'}
        ]
    """
    import chromadb
    configuration = Configuration.from_runnable_config()
    # import chromadb
    client = await chromadb.AsyncHttpClient(host='localhost', port=8000)
    collection = await client.get_or_create_collection(name="query_sql")
    query_results = await collection.query(query_texts=[query], n_results=5)
    if query_results is None:
        return []

    if "documents" in query_results:
        documents = query_results["documents"]
        if len(documents) == 1 and isinstance(documents[0], list):
            try:
                documents = [json.loads(doc) for doc in documents[0]]
            except Exception as e:
                return []

        return documents

def build_db_tools() -> List[Union[BaseTool, Callable, dict[str, Any]]]:
    """
    构建完整的工具系统（整合SQL工具和搜索工具）
    
    Args:
        config: 系统配置对象
        db: 已初始化的数据库连接
        llm: 语言模型实例
        
    Returns:
        整合后的工具列表

    """
    configuration = Configuration.from_runnable_config()
    db = from_duckdb()
    llm = load_chat_model(configuration.model)
    # 初始化SQL工具链
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    """构建兼容Callable的工具列表"""
    # 获取SQL工具集
    sql_tools = sql_toolkit.get_tools()

    # get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")

    # run_query_tool = next(tool for tool in tools if tool.name == "sql_db_query")
    
    # 合并工具系统
    return sql_tools


TOOLS: List[Callable[..., Any]] = build_db_tools() + [upper_text, example_selector, web_search]


