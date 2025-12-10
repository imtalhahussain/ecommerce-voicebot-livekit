# rag/build_index.py
from rag.vector_store import ProductVectorStore

def main():
    store = ProductVectorStore()
    store.build_index()

if __name__ == "__main__":
    main()
