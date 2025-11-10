import spacy
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel

nlp = spacy.load("en_core_web_sm")

@torch.no_grad()
def embed_sentences(sentences):
    embs = []
    for s in sentences:
        enc = bert_tokenizer(s, return_tensors="pt", truncation=True, max_length=512).to(device)
        out = bert_model(**enc)
        embs.append(out.last_hidden_state[:, 0, :].cpu().numpy())  # CLS token
    return np.vstack(embs)

def summarize(text: str, compression_ratio=0.4, min_sentences=3, max_sentences=None):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    # Calculate dynamic number of sentences based on input length
    num_sentences = max(min_sentences, int(len(sentences) * compression_ratio))
    
    # Apply max limit if specified
    if max_sentences:
        num_sentences = min(num_sentences, max_sentences)
    
    # If input is already short, return as-is
    if len(sentences) <= num_sentences:
        return text

    # get embeddings
    sent_embs = embed_sentences(sentences)
    doc_emb = sent_embs.mean(axis=0, keepdims=True)

    # rank by similarity to doc
    sims = cosine_similarity(sent_embs, doc_emb).ravel()
    top_ids = sims.argsort()[-num_sentences:]
    top_ids.sort()  

    summary = " ".join(sentences[i] for i in top_ids)
    return summary

def all_length(text):
    for length in range(3):
        match length:
            case 0:
                compression_ratio = 0.2
            case 1:
                compression_ratio = 0.4
            case 2:
                compression_ratio = 0.65
            case _:
                compression_ratio = 0.4
        
        summary = summarize(text, compression_ratio)

        print(summary)
        print(compression_ratio, len(summary.split()))
        print()


device = None or ("cuda" if torch.cuda.is_available() else "cpu")
bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
bert_model = AutoModel.from_pretrained("bert-base-uncased").to(device)

print("Setup done.")
text = input("")
print(len(text.split()))
# all_length(text)
length = int(input("1 - short | 2 - medium | 3 - long\n"))
print()

match length:
    case 1:
        compression_ratio = 0.2
    case 2:
        compression_ratio = 0.4
    case 3:
        compression_ratio = 0.65
    case _:
        compression_ratio = 0.4

# Extract sentences, with at least 3 and at most 10
summary = summarize(text, compression_ratio, min_sentences=3, max_sentences=10)

print(summary)
print()