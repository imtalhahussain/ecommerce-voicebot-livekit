# rag/vector_store.py
import faiss
import numpy as np
import json
from pathlib import Path
from rag.embeddings import embed_text

DATA_PATH = Path(__file__).parent / "product_data.json"
INDEX_PATH = Path(__file__).parent / "faiss.index"

class ProductVectorStore:
    def __init__(self):
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"product_data.json not found at {DATA_PATH}")
        self.products = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        self.index = None

    def build_index(self):
        vectors = []
        for p in self.products:
            text = (p.get("name", "") or "") + " " + (p.get("description", "") or "")
            vec = embed_text(text)
            vectors.append(vec)

        vectors = np.array(vectors).astype("float32")
        dim = vectors.shape[1]

        index = faiss.IndexFlatL2(dim)
        index.add(vectors)
        self.index = index

        faiss.write_index(index, str(INDEX_PATH))
        print("FAISS index built and saved at:", INDEX_PATH)

    def load_index(self):
        if not INDEX_PATH.exists():
            raise FileNotFoundError("FAISS index not found. Run build_index first.")
        self.index = faiss.read_index(str(INDEX_PATH))

    def search(self, query: str, k: int = 3):
        if self.index is None:
            raise RuntimeError("Index not loaded. Call load_index() first.")
        vec = np.array([embed_text(query)]).astype("float32")
        D, I = self.index.search(vec, k)
        results = []
        for idx in I[0]:
            results.append(self.products[int(idx)])
        return results
