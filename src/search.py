from qdrant_client import QdrantClient
from news_embeddings import get_titles_embeddings
from prefect import task
from qdrant_client.http.models import SearchRequest

client = QdrantClient(url="http://localhost:6333")

@task
def search(title_embeddings):
    requests = [
        SearchRequest(
            vector=embedding,
            limit=1,  # Number of results to return
            with_payload=True,  # Include metadata in the results
        )
        for embedding in title_embeddings
    ]

    result = client.search_batch(requests=requests, collection_name="news_embeddings")
    return result