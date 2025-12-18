import httpx
from agent.config import BACKEND_URL

class ProductSearchAPITool:
    name = "search_products"

    async def run(self, query: str):
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{BACKEND_URL}/products/search",
                json={"query": query, "limit": 3}
            )
            return r.json()
