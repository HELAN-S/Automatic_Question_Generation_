#get_tokenizer.py
from transformers import DistilBertTokenizerFast

tokenizer = DistilBertTokenizerFast.from_pretrained(
    "distilbert-base-uncased"
)

tokenizer.save_pretrained("models/bloom_model")

print("Tokenizer saved successfully")
