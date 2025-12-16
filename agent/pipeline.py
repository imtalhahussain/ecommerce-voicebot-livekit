from __future__ import annotations
import asyncio
from typing import Any

from .tools.rag_product_search import RAGProductSearchTool
from .intent import is_product_query

class VoicePipeline:
    def __init__(self, stt, llm, tts):
        self.stt = stt
        self.llm = llm
        self.tts = tts
        self.rag_tool = RAGProductSearchTool()

    async def handle_audio_turn(self, audio_bytes: bytes) -> dict[str, Any]:
        # 1. STT
        transcript = await self.stt.transcribe(audio_bytes)
        transcript = (transcript or "").strip()

        # 2. RAG
        rag_results = None
        if transcript and is_product_query(transcript):
            try:
                rag_results = await self.rag_tool.run(transcript)
            except Exception as e:
                print("RAG error:", e)

        # 3. Prompt
        prompt = f"""
You are an AI shopping assistant.

User: {transcript}
"""

        if rag_results:
            prompt += "\nProducts:\n"
            for p in rag_results.get("results", []):
                prompt += f"- {p['name']} | ₹{p['price']}\n"

        # 4. LLM
        reply_text = await self.llm.chat(prompt)
        reply_text = reply_text.strip()

        # 5. TTS (IMPORTANT: await)
        reply_audio = await self.tts.synthesize(reply_text)

        return {
            "user_transcript": transcript,
            "assistant_reply_text": reply_text,
            "assistant_reply_audio": reply_audio,
        }
