from __future__ import annotations
import os
import httpx
from typing import Any, Dict

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

class ProductSearchAPITool:
    name = "search_products_api"
    description = "Call backend /products/search and return product results."

    async def run(self, query: str, max_price: float | None = None, category: str | None = None, size: str | None = None) -> Dict[str, Any]:
        payload = {
            "query": query,
            "max_price": max_price,
            "category": category,
            "size": size,
            "limit": 5
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{BACKEND_URL}/products/search", json=payload)
            resp.raise_for_status()
            return resp.json()
