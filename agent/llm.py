import os
import json
from google import genai

from agent.tools.product_search_api import ProductSearchAPITool
from agent.tools.order_status_api import OrderStatusAPITool


class GeminiAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.product_tool = ProductSearchAPITool()
        self.order_tool = OrderStatusAPITool()

    async def respond(self, user_text: str, history: list) -> str:
        system_prompt = """
You are an ecommerce voice assistant.

If a tool is needed, respond ONLY in JSON.

Product search:
{
  "tool": "search_products",
  "args": { "query": "..." }
}

Order status:
{
  "tool": "get_order_status",
  "args": { "order_id": "ORD123" }
}

Otherwise respond normally.
"""

        prompt = system_prompt + "\n"
        for h in history:
            prompt += f"{h['role']}: {h['content']}\n"
        prompt += f"user: {user_text}\nassistant:"

        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )

        text = response.text.strip()

        if text.startswith("{"):
            try:
                call = json.loads(text)

                if call["tool"] == "search_products":
                    result = await self.product_tool.run(**call["args"])
                    return f"I found these products: {result.get('results', [])}"

                if call["tool"] == "get_order_status":
                    result = await self.order_tool.run(**call["args"])
                    return f"Here is your order status: {result}"

            except Exception:
                return "Sorry, something went wrong while fetching details."

        return text
