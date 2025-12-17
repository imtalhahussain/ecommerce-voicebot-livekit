from agent.config import BACKEND_URL
import httpx
from typing import Any, Dict


class ProductSearchAPITool:
    name = "search_products_api"
    description = "Call backend /products/search and return product results."

    async def run(
        self,
        query: str,
        max_price: float | None = None,
        category: str | None = None,
        size: str | None = None,
    ) -> Dict[str, Any]:

        payload = {
            "query": query,
            "max_price": max_price,
            "category": category,
            "size": size,
            "limit": 5,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{BACKEND_URL}/products/search", json=payload)
            resp.raise_for_status()
            return resp.json()
