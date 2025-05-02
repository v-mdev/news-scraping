import polars as pl
from transformers import AutoTokenizer, AutoModel
import torch


news_category = [
    "Política",
    "Economía",
    "Deportes",
    "Tecnología",
    "Salud",
    "Ciencia",
    "Entretenimiento",
    "Cultura",
    "Internacional",
    "Sociedad",
    "Medio Ambiente",
    "Educación",
    "Viajes"
]







# Load model from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Tokenize sentences
encoded_input = tokenizer(news_category, padding=True, truncation=True, return_tensors='pt')

# Compute token embeddings
with torch.no_grad():
    model_output = model(input_ids=encoded_input["input_ids"], attention_mask=encoded_input["attention_mask"])

news_category_embeddings = model_output[0][:,0,:]

print("Sentence embeddings:")
print(news_category_embeddings)
print(news_category_embeddings.size())