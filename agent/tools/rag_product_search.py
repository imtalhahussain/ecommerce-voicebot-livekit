# agent/tools/rag_product_search.py
from __future__ import annotations
import os
import httpx
from typing import Any, Dict

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

class RAGProductSearchTool:
    """
    Calls backend POST /products/search
    """

    name = "rag_product_search"
    description = "Search products from backend using RAG"

    async def run(self, query: str) -> Dict[str, Any]:
        payload = {
            "query": query,
            "max_price": 3000,
            "limit": 5
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{BACKEND_URL}/products/search",
                json=payload
            )
            resp.raise_for_status()
            return resp.json()
