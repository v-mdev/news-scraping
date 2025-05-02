from transformer import get_news_category_embeddings
import polars as pl
from qdrant_client import QdrantClient
from prefect import task
from transformer import get_news_category_embeddings
from qdrant_client.models import VectorParams, Distance
import numpy as np
from qdrant_client.models import PointStruct


def from_zip_to_list(embedding):
    result_list = []
    i = 0
    for (tensor, news) in embedding:
        result_list.append([tensor.tolist(), news, i])
        i = i+1
    return result_list


client = QdrantClient(url="http://localhost:6333")

@task
def create_collection_if_not_exists():
  if not client.collection_exists("news_embeddings"):
    client.create_collection(
        collection_name="news_embeddings",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )


@task
def insert_embeddings(embeddings):
  client.upsert(
    collection_name="news_embeddings",
    points=[
        PointStruct(
              vector=vector,
              payload={"news": news},
              id=id
        )
        for vector, news, id in from_zip_to_list(embeddings)
    ]
  )



collection_name="news_embeddings"
dimension=384
metric_type="COSINE"



# create_collection_if_not_exists()
# print(insert_embeddings(get_news_category_embeddings()))

# scroll_result = client.scroll(
#     collection_name="news_embeddings",
#     limit=10,  # Número de puntos a recuperar por iteración
#     with_payload=True,  # Incluir los metadatos (payload)
#     with_vectors=True   # Incluir los vectores
# )

# # Imprimir los resultados
# for point in scroll_result[0]:  # scroll_result[0] contiene los puntos
#     print(f"ID: {point.id}, Vector: {point.vector}, Payload: {point.payload}")