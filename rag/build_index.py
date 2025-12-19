import json
import faiss
import numpy as np

from rag.embeddings import embed

INDEX_PATH = "rag/faiss.index"
DATA_PATH = "rag/product_data.json"


def build():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    texts = [
        f"{p['name']} - {p.get('description', '')}"
        for p in products
    ]

    vectors = embed(texts)
    dim = vectors.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(np.array(vectors).astype("float32"))

    faiss.write_index(index, INDEX_PATH)
    print("FAISS index built")


if __name__ == "__main__":
    build()
