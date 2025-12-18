from groq import Groq
from agent.config import GROQ_API_KEY


class GroqAgent:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    async def reply(self, user_text: str, memory):
        """
        Generate a reply using Groq with conversation memory.
        """

        messages = []

        # load conversation memory
        for msg in memory.last(6):
            messages.append({
                "role": "user" if msg["role"] == "user" else "assistant",
                "content": msg["parts"][0]["text"]
            })

        # DO NOT append user_text again if memory already has it
        # (livekit_agent already added it)

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.4,
        )

        return response.choices[0].message.content.strip()
