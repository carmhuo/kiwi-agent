import os
import time
from concurrent.futures import ThreadPoolExecutor, Executor
import asyncio
from contextvars import ContextVar, copy_context
from functools import partial

from langchain_core.runnables import RunnableConfig

var_child_runnable_config: ContextVar[RunnableConfig | None] = ContextVar(
    "child_runnable_config", default=None
)

query = """
    SELECT count(*) as total_customers FROM  tpch_sf1.customer;
"""

question = "show me the pie chart of the market share in customer table"

runnable_config = {
    "run_id": "2025",
    "run_name": "test",
    "max_concurrency": 4,
    "configurable": {
        "model": "QWEN3_32B",
        "chromadb_path": "C:\\Users\\si929x\\Desktop\\projects\\kiwi\\data\\chroma_db",
        "duckdb_path": "C:\\Users\\si929x\\Desktop\\projects\\kiwi\\data\\tpch_sf1.db"
    }
}


def duckdb_query(query) -> list:
    print("DuckDB context: ", var_child_runnable_config.get())
    import duckdb
    duckdb_path = os.getenv('DUCKDB_PATH')
    with duckdb.connect(duckdb_path) as conn:
        try:
            rl = conn.sql(query)
            result = rl.fetchall()
            time.sleep(2)
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            return []


async def run_anther_task():
    print("Task2 started")
    print("Task2 context: ", var_child_runnable_config.get())
    await asyncio.sleep(1)
    print("Task2 finished")
    return "OK"


def chromadb_query(query):
    print("ChromaDB context: ", var_child_runnable_config.get())
    import chromadb
    persist_dir = os.getenv('CHROMADB_PATH')
    # persist_dir = "C:\\Users\\si929x\\Desktop\\projects\\kiwi\\data\\chroma_db"
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    collection = chroma_client.get_or_create_collection("2025_userspace_query_examples")
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results


async def run_in_executor(executor_or_config: ThreadPoolExecutor | RunnableConfig | None, func, *args):
    """通用任务执行方法"""
    loop = asyncio.get_running_loop()
    if executor_or_config is None or isinstance(executor_or_config, dict):
        # Use default executor with context copied from current context
        return await loop.run_in_executor(
            None,
            copy_context().run(func, *args)
        )
    result = await loop.run_in_executor(executor_or_config, func, *args)
    return result


async def main():
    """主协程：并行运行两个任务"""

    os.environ['CHROMADB_PATH'] = runnable_config['configurable']['chromadb_path']
    os.environ['DUCKDB_PATH'] = runnable_config['configurable']['duckdb_path']
    var_child_runnable_config.set(runnable_config)
    # 并行创建三个任务
    task1 = asyncio.create_task(run_in_executor(executor, duckdb_query, query))
    task2 = asyncio.create_task(run_anther_task())
    task3 = asyncio.create_task(run_in_executor(executor, chromadb_query, question))

    try:
        result1, result2, result3 = await asyncio.wait_for(asyncio.gather(task1, task2, task3), timeout=10)
        print("Database result:", result1)
        print("Other task result:", result2)
        print("Chromadb result:", result3)
    except asyncio.TimeoutError:
        print("任务执行超时")
    except Exception as e:
        print(f"Error during task execution: {e}")
    finally:
        # 显式关闭线程池
        executor.shutdown(wait=True, cancel_futures=True)
        print("线程池已关闭")
        # chromadb 无法释放Windows 文件锁，需强制释放
        if os.name == 'nt':
            try:
                os.system("taskkill /f /im python.exe")
            except:
                pass
    # 检查线程池状态
    if executor._work_queue.qsize() > 100:
        print("线程池任务积压!")


# 创建线程池执行器：
executor = ThreadPoolExecutor(max_workers=4)

# 运行主程序
asyncio.run(main(), debug=True)
