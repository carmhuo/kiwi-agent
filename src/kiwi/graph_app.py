import os
from typing import Union, Tuple
import pandas as pd
import plotly.graph_objs
from kiwi.flask_app import VannaFlaskApp
from kiwi.core import ChromaDB_VectorStore
from kiwi.core import LangChain_Chat
from kiwi.utils import find_free_port, load_chat_model
try:
    from kiwi.react_agent.graph import graph
except ImportError:
    print("⚠️  React agent graph not available, using basic functionality")

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


class MyKiwi(ChromaDB_VectorStore, LangChain_Chat):
    def __init__(self, chat_model=None, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        LangChain_Chat.__init__(self, chat_model=chat_model, config=config)


    def ask_with_graph(
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
        vn.ask_with_graph("What are the top 10 customers by sales?")
        ```

        Ask using LangGraph agent for enhanced reasoning.

        Args:
            question (str): The question to ask.
            print_results (bool): Whether to print the results of the SQL query.
            auto_train (bool): Whether to automatically train Vanna.AI on the question and SQL query.
            visualize (bool): Whether to generate plotly code and display the plotly figure.

        Returns:
            Tuple[str, pd.DataFrame, plotly.graph_objs.Figure]: The SQL query, the results of the SQL query, and the plotly figure.
        """
        if question is None:
            return None
            
        try:
            # Use LangGraph agent if available
            if 'graph' in globals():
                for step in graph.stream(
                    {"messages": [{"role": "user", "content": question}]},
                    stream_mode="values",
                ):
                    step["messages"][-1].pretty_print()
            else:
                # Fallback to regular ask method
                return self.ask(question, print_results, auto_train, visualize, allow_llm_to_see_data)
        except Exception as e:
            print(f"Graph processing failed: {e}, falling back to regular ask")
            return self.ask(question, print_results, auto_train, visualize, allow_llm_to_see_data)

    
def main():
    print("🚀 Starting Kiwi Graph Application...")
    model = os.getenv('MODELSCOPE_DEEPSEEK_MODEL')
    # Initialize Vanna with configuration
    kiwi = MyKiwi(chat_model=load_chat_model(model), config={
        'path': '/mnt/workspace/data/chromadb/tpch_db', 
        'client': 'persistent', 
        'n_results_sql': 5
    })

    # Connect to database
    db_path = '/mnt/workspace/data/duckdb/tpch_sf1.db'
    if os.path.exists(db_path):
        print(f"📊 Connecting to database: {db_path}")
        kiwi.connect_to_duckdb(db_path, read_only=True)
    else:
        print(f"⚠️  Database not found: {db_path}")
        print("💡 Application will run but database features may not work.")

    # Create Flask app with LangGraph integration
    app = VannaFlaskApp(
        kiwi, 
        logo=None, 
        title="Welcome to Kiwi", 
        allow_llm_to_see_data=True, 
        debug=True
    )
    
    print("🌐 Starting Flask application with LangGraph support...")
    print("🌍 Access the application at: http://0.0.0.0:12000")
    print("🔄 Press Ctrl+C to stop the server")
    
    # Run with reloader disabled to prevent restart issues
    app.run(host='0.0.0.0', port=12000, debug=True, use_reloader=False)

if __name__ == "__main__":
    main()