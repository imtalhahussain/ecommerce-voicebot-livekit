from __future__ import annotations
import os
import httpx
from typing import Any, Dict

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

class RAGProductSearchTool:
    """
    Calls POST /products/search on backend.
    """

    name = "rag_product_search"
    description = "Search products using backend catalog"

    async def run(self, query: str) -> Dict[str, Any]:
        payload = {
            "query": query,
            "limit": 5
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{BACKEND_URL}/products/search",
                json=payload
            )
            resp.raise_for_status()
            return resp.json()
