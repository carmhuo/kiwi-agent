from kiwi.flask_app import VannaFlaskApp
from kiwi import ChromaDB_VectorStore
from kiwi import OpenAI_Chat
from openai import OpenAI

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1/',
    api_key='9d431c1c-2acd-4dd0-b95a-76affce19b3b', # ModelScope Token
)

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)

vn = MyVanna(config={'model' : 'Qwen/Qwen2.5-32B-Instruct', 'path' : '/mnt/workspace/data/chroma_db', 'client' : 'persistent', 'n_results_sql' : 5})

vn.connect_to_duckdb('/mnt/workspace/data/duckdb/tpch_sf1.db', read_only=True)

app = VannaFlaskApp(vn, logo=None, title="Welcome to Carmhuo", allow_llm_to_see_data=True, debug=True,)
app.run(host='0.0.0.0', port=12000, debug=True)