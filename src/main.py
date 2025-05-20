from prefect import flow
from docker_utils import start_qdrant
from extract import process_urls, urls
from transformer import get_news_category_embeddings
from load_emb import create_collection_if_not_exists, insert_embeddings
from news_embeddings import get_titles_embeddings, news_category
from search import search


@flow
def pipeline():
    start_qdrant()

    process_urls(urls)
    news_embeddings = get_news_category_embeddings()

    create_collection_if_not_exists()
    insert_embeddings(news_embeddings)

    title_embeddings = get_titles_embeddings()
    result = search(title_embeddings)

    news_classified = news_category(result)
    news_classified.write_csv('news_classified.csv')

if __name__ == "__main__":
    pipeline()