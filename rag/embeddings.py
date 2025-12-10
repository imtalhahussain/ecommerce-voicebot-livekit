# rag/embeddings.py
from sentence_transformers import SentenceTransformer

# lightweight embedding model (downloads first time)
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    """Return a list[float] embedding for the text."""
    return _model.encode(text)
