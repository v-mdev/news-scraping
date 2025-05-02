import polars as pl
from transformers import AutoTokenizer, AutoModel
import torch
from prefect import task

news = pl.read_csv("news.csv")

list_titles = news.get_column("title").to_list()

# Load model from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

#@task
def get_titles_embeddings():
    # Tokenize sentences
    encoded_input = tokenizer(list_titles, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(input_ids=encoded_input["input_ids"], attention_mask=encoded_input["attention_mask"])

    # Extract CLS token embeddings
    titles_embeddings = model_output[0][:, 0, :]
    return titles_embeddings.tolist()