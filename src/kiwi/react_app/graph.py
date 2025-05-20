import os

from langchain_openai import ChatOpenAI
from typing import Literal
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

# db = SQLDatabase.from_uri("sqlite:////mnt/workspace/data/Chinook.db")
# 创建 DuckDB 连接，并设置为只读模式
engine = create_engine(
    "duckdb:////mnt/workspace/data/duckdb/tpch_sf1.db",
    connect_args={
        "read_only": True  # 设置为只读模式
    }
)
db = SQLDatabase(engine=engine)

print(db.dialect)
print(db.get_usable_table_names())

llm = ChatOpenAI(
    model=os.getenv("MODELSCOPE_MODEL"),
    base_url=os.getenv("MODELSCOPE_API_BASE"),
    api_key=os.getenv("MODELSCOPE_API_KEY"),  # ModelScope Token
    temperature=0
)


toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

for tool in tools:
    print(f"{tool.name}: {tool.description}\n")
    
from langgraph.prebuilt import create_react_agent

system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect=db.dialect,
    top_k=5,
)

agent = create_react_agent(
    llm,
    tools,
    prompt=system_prompt,
)

# question = "Which sales agent made the most in sales in 2009?"

# for step in agent.stream(
#     {"messages": [{"role": "user", "content": question}]},
#     stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()