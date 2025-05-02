from transformer import get_news_category_embeddings
import polars as pl
from pymilvus import MilvusClient

client = MilvusClient("news.db")

if not client.has_collection("news_embeddigs"):
    client.create_collection(
    collection_name="news_embeddings",
    dimension=13
    )

insert = client.insert(
  collection_name="news_embeddings",
  data=get_news_category_embeddings
)