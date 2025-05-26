import os
import sys
import socket
from kiwi.flask_app import VannaFlaskApp
from kiwi import ChromaDB_VectorStore
from kiwi import OpenAI_Chat
from openai import OpenAI

def find_free_port():
    """Find an available port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

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

        class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
            def __init__(self, config=None):
                ChromaDB_VectorStore.__init__(self, config=config)
                OpenAI_Chat.__init__(self, client=client, config=config)

        print("🧠 Initializing Vanna AI...")
        vn = MyVanna(config={
            'model': 'Qwen/Qwen2.5-32B-Instruct', 
            'path': '/mnt/workspace/data/chroma_db', 
            'client': 'persistent', 
            'n_results_sql': 5
        })

        # Connect to database
        db_path = '/mnt/workspace/data/duckdb/tpch_sf1.db'
        if os.path.exists(db_path):
            print(f"📊 Connecting to database: {db_path}")
            vn.connect_to_duckdb(db_path, read_only=True)
        else:
            print(f"⚠️  Database not found: {db_path}")
            print("💡 Application will run but database features may not work.")

        print("🌐 Creating Flask application...")
        app = VannaFlaskApp(
            vn, 
            logo=None, 
            title="Welcome to Carmhuo Kiwi SQL Assistant", 
            allow_llm_to_see_data=True, 
            debug=True
        )

        # Find available port
        port = find_free_port()
        print(f"🎯 Starting server on port {port}...")
        print(f"🌍 Access the application at: http://localhost:{port}")
        print("🔄 Press Ctrl+C to stop the server")
        
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)

    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("🔧 Troubleshooting tips:")
        print("   1. Check your ModelScope API key")
        print("   2. Verify internet connection")
        print("   3. Check if all dependencies are installed")
        sys.exit(1)

if __name__ == "__main__":
    main()