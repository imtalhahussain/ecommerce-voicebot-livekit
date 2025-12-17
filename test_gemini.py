from dotenv import load_dotenv
load_dotenv()

import asyncio


from agent.models.llm import GeminiLLM

async def main():
    llm = GeminiLLM()
    reply = await llm.chat("Say hello in one sentence")
    print(reply)

asyncio.run(main())
