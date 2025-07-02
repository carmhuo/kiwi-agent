import asyncio
import pytest
import json
from dotenv import load_dotenv

async def example_selector(query: str):
    """
    如果我们有足够的示例，我们可能希望在提示中只包含最相关的示例，要么是因为它们不适合模型的上下文窗口，要么是因为示例的长尾会分散模型的注意力。
    给定任何输入，我们都希望包含与该输入最相关的示例。
    Args:
        query:

    Returns:
        List[str] or None: The extracted documents, or an empty list or
        single document if an error occurred.
    Examples:
        [{'input': 'List all artists.', 'query': 'SELECT * FROM Artist;'},
         {'input': 'How many employees are there','query': 'SELECT COUNT(*) FROM "Employee"'},
         {'input': 'How many tracks are there in the album with ID 5?',
          'query': 'SELECT COUNT(*) FROM Track WHERE AlbumId = 5;'}
        ]
    """

    import chromadb
    client = await chromadb.AsyncHttpClient()
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
                return documents[0]
        return documents


async def main():
    print("Hello")
    res = await example_selector("total sales for each region?")

    print(res)


def test():
    load_dotenv(override=True)  # load environment variables from .env
    asyncio.run(main())

