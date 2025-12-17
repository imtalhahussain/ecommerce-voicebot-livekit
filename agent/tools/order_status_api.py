from agent.config import BACKEND_URL
import httpx
from typing import Any, Dict


class OrderStatusAPITool:
    name = "get_order_status_api"
    description = "Call backend /orders/{order_id} and return order info."

    async def run(self, order_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{BACKEND_URL}/orders/{order_id}")
            if resp.status_code == 404:
                return {"error": "order_not_found", "order_id": order_id}
            resp.raise_for_status()
            return resp.json()
