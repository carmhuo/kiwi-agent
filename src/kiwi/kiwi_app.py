import os
import sys
import socket
from datetime import datetime

from kiwi.flask_app import VannaFlaskApp
from kiwi import ChromaDB_VectorStore
from kiwi import OpenAI_Chat
from openai import OpenAI


class MyKiwi(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, client=None, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)


def find_free_port(default_port=2025):
    """Find an available port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', default_port))
            s.listen(1)
            return default_port
        except socket.error:
            s.bind(('', 0))
            s.listen(1)
            return s.getsockname()[1]
    return port

def _duckdb_init_sql() ->  str:
    """ Get database init script path from environment"""
    init_sql = None
    init_script_path = os.getenv('DUCKDB_INIT_SCRIPT')

    if init_script_path and os.path.exists(init_script_path):
        try:
            with open(init_script_path, 'r') as f:
                init_sql = f.read()
            print(f"✅ Loaded duckdb initialization script from {init_script_path}")
            return init_sql
        except Exception as e:
            print(f"❌ Failed to read init script: {str(e)}")
            sys.exit(1)
    return None

def main():
    print("🚀 Starting Kiwi Application...")

    # Load environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("⚠️  dotenv not available, using system environment variables")

    # Get API key from environment variable
    api_key = os.getenv('MODELSCOPE_API_KEY')
    if not api_key:
        print("❌ MODELSCOPE_API_KEY environment variable is required.")
        print("💡 Please set it with: export MODELSCOPE_API_KEY='your-api-key'")
        print("📖 Or add it to the .env file: MODELSCOPE_API_KEY=your-api-key")
        sys.exit(1)

    try:
        print("🔗 Connecting to ModelScope API...")
        client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1/',
            api_key=api_key,  # ModelScope Token from environment
        )

        print("🧠 Initializing Kiwi AI...")

        formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        initial_prompt = """
        You are a {dialect} expert.
        Please help to generate a syntactically correct SQL query to answer the question. 
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.

        Your response should ONLY be based on the given context and follow the response guidelines and format instructions.

        Today is {current_time}.
        """.format(
            dialect='duckdb',
            top_k=1000,
            current_time=formatted_time,
        )
        model = os.getenv('MODELSCOPE_DEEPSEEK_MODEL')
        chroma_path = '/mnt/workspace/data/chromadb/gb_vhcl_signal_db'

        kiwi = MyKiwi(client=client, config={
            'model': model,
            'path': chroma_path,
            'client': 'persistent',
            'n_results_sql': 5,
            'initial_prompt': initial_prompt
        })

        # Connect to duckdb
        db_path = '/mnt/workspace/data/duckdb/gb_vhcl.db'
        if os.path.exists(db_path):
            print(f"📊 Connecting to database: {db_path}")
            kiwi.connect_to_duckdb(db_path, init_sql=_duckdb_init_sql(), read_only=True)
        else:
            print(f"⚠️  Database not found: {db_path}")
            print("💡 Application will run but database features may not work.")

        print("🌐 Creating Flask application...")
        app = VannaFlaskApp(
            kiwi, 
            logo=None, 
            title="Welcome to Kiwi SQL Assistant", 
            allow_llm_to_see_data=True, 
            debug=False
        )

        # Find available port
        port = find_free_port()
        print(f"🎯 Starting server on port {port}...")
        print(f"🌍 Access the application at: http://localhost:{port}")
        print("🔄 Press Ctrl+C to stop the server")

        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("🔧 Troubleshooting tips:")
        print("   1. Check your ModelScope API key")
        print("   2. Verify internet connection")
        print("   3. Check if all dependencies are installed")
        sys.exit(1)


if __name__ == "__main__":
    main()