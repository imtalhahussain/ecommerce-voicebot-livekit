import httpx
from agent.config import BACKEND_URL

class OrderStatusAPITool:
    name = "get_order_status"

    async def run(self, order_id: str):
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{BACKEND_URL}/orders/{order_id}")
            if r.status_code == 404:
                return {"error": "Order not found"}
            return r.json()
