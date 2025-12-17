class MockLLM:
    async def chat(self, prompt: str) -> str:
        return "Sure! I found some running shoes under 3000 rupees."
