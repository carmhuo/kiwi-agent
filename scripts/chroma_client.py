import chromadb
import json
import os
from chromadb.utils import embedding_functions
from datetime import datetime
from typing import List

from kiwi.utils import deterministic_uuid
from kiwi.embedding import ONNXMiniLM_L6_V2

embedding = ONNXMiniLM_L6_V2()


def simple_test():
    chroma_client = chromadb.Client()

    # Default Embedding 模型（based on the Sentence Transformers all-MiniLM-L6-v2 model)
    # 使用默认 Sentence Transformers 函数（自动复用本地缓存）
    # embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(
    #     model_name="all-MiniLM-L6-v2"
    # )
    embedding_model = embedding_functions.DefaultEmbeddingFunction()

    collection = chroma_client.get_or_create_collection(name="query_sql",  configuration={"embedding_function": embedding_model},
                                                 metadata={
                                                        "description": "query examples",
                                                        "created": str(datetime.now())}
                                                )

    collection.add(
        documents=["This is a document about engineer", "This is a document about steak"],
        metadatas=[{"source": "doc1"}, {"source": "doc2"}],
        ids=["id1", "id2"]
    )

    results = collection.query(
        query_texts=["Which food is the best?"],
        n_results=2
    )

    print(results)

    # 查询某文档的向量
    result = collection.get(ids=["id1"], include=["embeddings"])
    print(len(result["embeddings"][0]))  # 应输出 384

examples = [
    {"input": "List all artists.", "query": "SELECT * FROM Artist;"},
    {
        "input": "Find all albums for the artist 'AC/DC'.",
        "query": "SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');",
    },
    {
        "input": "List all tracks in the 'Rock' genre.",
        "query": "SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');",
    },
    {
        "input": "Find the total duration of all tracks.",
        "query": "SELECT SUM(Milliseconds) FROM Track;",
    },
    {
        "input": "List all customers from Canada.",
        "query": "SELECT * FROM Customer WHERE Country = 'Canada';",
    },
    {
        "input": "How many tracks are there in the album with ID 5?",
        "query": "SELECT COUNT(*) FROM Track WHERE AlbumId = 5;",
    },
    {
        "input": "Find the total number of invoices.",
        "query": "SELECT COUNT(*) FROM Invoice;",
    },
    {
        "input": "List all tracks that are longer than 5 minutes.",
        "query": "SELECT * FROM Track WHERE Milliseconds > 300000;",
    },
    {
        "input": "Who are the top 5 customers by total purchase?",
        "query": "SELECT CustomerId, SUM(Total) AS TotalPurchase FROM Invoice GROUP BY CustomerId ORDER BY TotalPurchase DESC LIMIT 5;",
    },
    {
        "input": "Which albums are from the year 2000?",
        "query": "SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';",
    },
    {
        "input": "How many employees are there",
        "query": 'SELECT COUNT(*) FROM "Employee"',
    },
]


def generate_embedding(data: str, **kwargs) -> List[float]:
    _embedding = embedding.embed_documents([data])
    if len(_embedding) == 1:
        return _embedding[0]
    return _embedding



def index_from_json():
    import json

    # 打开 JSON 文件并加载内容
    with open('C:\\Users\\si929x\\Desktop\\projects\\kiwi\\data\\questions.json', 'r', encoding='utf-8') as file:
        questions = json.load(file)

    chroma_client = chromadb.PersistentClient(path='C:\\Users\\si929x\\Desktop\\projects\\kiwi\\data\\chroma_db')

    sql_collection = chroma_client.get_or_create_collection(name="query_sql",
                                             metadata={
                                                    "description": "query examples",
                                                    "created": str(datetime.now())}
                                            )

    def _add_question_sql(question: str, sql: str, **kwargs) -> str:
        question_sql_json = json.dumps(
            {
                "question": question,
                "sql": sql,
            },
            ensure_ascii=False,
        )
        id = deterministic_uuid(question_sql_json) + "-sql"

        sql_collection.add(
            documents=question_sql_json,
            embeddings=generate_embedding(question_sql_json),
            ids=id,
        )
        return id


    idx = []
    for example in questions:
        id = _add_question_sql(example['question'], example['answer'])
        idx.append(id)
    print(f"ids: {idx}")

    results = sql_collection.query(
        query_embeddings = generate_embedding("total sales for each region?"),
        n_results=2
    )

    print(results)

if __name__ == "__main__":
    index_from_json()
