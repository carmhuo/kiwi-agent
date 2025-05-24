"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast, Union
from functools import partial

from langchain_core.tools import BaseTool
from langchain_tavily import TavilySearch
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from kiwi.react_agent.configuration import Configuration

async def web_search(query: str) -> Optional[dict[str, Any]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    configuration = Configuration.from_context()
    wrapped = TavilySearch(max_results=configuration.max_search_results)
    return cast(dict[str, Any], await wrapped.ainvoke({"query": query}))

TOOLS: List[Callable[..., Any]] = [web_search]

def build_tool_system(
    db: SQLDatabase,
    llm: Any,
    config: Configuration
) -> List[Union[BaseTool, Callable, dict[str, Any]]]:
    """
    构建完整的工具系统（整合SQL工具和搜索工具）
    
    Args:
        config: 系统配置对象
        db: 已初始化的数据库连接
        llm: 语言模型实例
        
    Returns:
        整合后的工具列表
        
    Example:
        >>> config = Configuration.from_context()
        >>> db = load_database(config)
        >>> llm = load_llm(config.model)
        >>> tools = build_tool_system(config, db, llm)
    """
    # 初始化SQL工具链
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    """构建兼容Callable的工具列表"""
    # 获取SQL工具集
    sql_tools = sql_toolkit.get_tools()

    # get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")

    # run_query_tool = next(tool for tool in tools if tool.name == "sql_db_query")
    
    # 合并工具系统
    return sql_tools + TOOLS

