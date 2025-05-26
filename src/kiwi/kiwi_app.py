import os
from kiwi.flask_app import VannaFlaskApp
from kiwi import ChromaDB_VectorStore
from kiwi import OpenAI_Chat
from openai import OpenAI

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

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)

vn = MyVanna(config={'model' : 'Qwen/Qwen2.5-32B-Instruct', 'path' : '/mnt/workspace/data/chroma_db', 'client' : 'persistent', 'n_results_sql' : 5})

vn.connect_to_duckdb('/mnt/workspace/data/duckdb/tpch_sf1.db', read_only=True)

app = VannaFlaskApp(vn, logo=None, title="Welcome to Carmhuo", allow_llm_to_see_data=True, debug=True,)
app.run(host='0.0.0.0', port=12000, debug=True)