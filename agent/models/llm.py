from google import genai
from agent.config import GEMINI_API_KEY


class GeminiLLM:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    async def chat(self, message: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message,
        )
        return response.text.strip()
