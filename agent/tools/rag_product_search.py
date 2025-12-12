# agent/tools/rag_product_search.py
from __future__ import annotations
import os
import httpx
from typing import Any, Dict

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

class RAGProductSearchTool:
    """
    Async tool that calls the backend /rag/search endpoint.
    Returns JSON dict with keys: 'query' and 'results'.
    """

    name = "rag_product_search"
    description = "Call backend RAG product search and return top product matches."

    async def run(self, query: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{BACKEND_URL}/rag/search", params={"q": query})
            resp.raise_for_status()
            return resp.json()
