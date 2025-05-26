import os
from kiwi.flask_app import VannaFlaskApp
from kiwi import ChromaDB_VectorStore
from kiwi import OpenAI_Chat
from openai import OpenAI
from react_agent import graph

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# Get API key from environment variable
api_key = os.getenv('MODELSCOPE_API_KEY')
if not api_key:
    raise ValueError(
        "MODELSCOPE_API_KEY environment variable is required. "
        "Please set it with: export MODELSCOPE_API_KEY='your-api-key'"
    )

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1/',
    api_key=api_key,  # ModelScope Token from environment
)

class Kiwi(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)

    def ask(
        self,
        question: Union[str, None] = None,
        print_results: bool = True,
        auto_train: bool = True,
        visualize: bool = True,  # if False, will not generate plotly code
        allow_llm_to_see_data: bool = False,
    ) -> Union[
        Tuple[
            Union[str, None],
            Union[pd.DataFrame, None],
            Union[plotly.graph_objs.Figure, None],
        ],
        None,
    ]:
        """
        **Example:**
        ```python
        vn.ask("What are the top 10 customers by sales?")
        ```

        Ask Vanna.AI a question and get the SQL query that answers it.

        Args:
            question (str): The question to ask.
            print_results (bool): Whether to print the results of the SQL query.
            auto_train (bool): Whether to automatically train Vanna.AI on the question and SQL query.
            visualize (bool): Whether to generate plotly code and display the plotly figure.

        Returns:
            Tuple[str, pd.DataFrame, plotly.graph_objs.Figure]: The SQL query, the results of the SQL query, and the plotly figure.
        """
    for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()

    
vn = MyVanna(config={'model' : 'Qwen/Qwen2.5-32B-Instruct', 'path' : '/mnt/workspace/data/chromadb/tpch_db', 'client' : 'persistent', 'n_results_sql' : 5})

vn.connect_to_duckdb('/mnt/workspace/data/duckdb/tpch_sf1.db', read_only=True)

app = VannaFlaskApp(vn, logo=None, title="Welcome to LangGraph", allow_llm_to_see_data=True, debug=True,)
app.run()