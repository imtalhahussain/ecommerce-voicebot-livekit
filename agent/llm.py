from groq import Groq
from agent.config import GROQ_API_KEY
from rag.vector_store import rag_search


class GroqAgent:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    async def reply(self, user_text: str, memory):
        """
        Generate a reply using Groq with conversation memory
        and backend-style order lookup.
        """

        # ---- Backend action: Order lookup (RAG / tool call) ----
        rag_result = rag_search(user_text)
        if rag_result:
            return rag_result

        # ---- Build conversation context ----
        messages = []

        for msg in memory.as_messages():
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.4,
        )

        return response.choices[0].message.content.strip()
