from __future__ import annotations
import asyncio
from typing import Any

from .tools.rag_product_search import RAGProductSearchTool
from .intent import is_product_query
from .memory import ConversationMemory


class VoicePipeline:
    def __init__(self, stt, llm, tts):
        self.stt = stt
        self.llm = llm
        self.tts = tts
        self.rag_tool = RAGProductSearchTool()
        self.memory = ConversationMemory()

    async def handle_audio_turn(self, audio_bytes: bytes) -> dict[str, Any]:
        # 1️⃣ Speech → Text
        transcript = await self.stt.transcribe(audio_bytes)
        transcript = (transcript or "").strip()

        rag_results = None

        # 2️⃣ Intent + RAG
        if transcript and is_product_query(transcript):
            try:
                rag_results = await self.rag_tool.run(transcript)
            except Exception as e:
                print("RAG tool error:", repr(e))

        # 3️⃣ Build STRUCTURED PROMPT (IMPORTANT)
        history = self.memory.recent()

        prompt = """
You are an AI shopping assistant for an e-commerce platform.

Rules:
- Be concise (2–3 lines)
- Recommend products clearly
- Use prices when available
- Ask follow-up questions if needed
"""

        prompt += "\nConversation history:\n"
        for h in history:
            prompt += f"{h['role'].capitalize()}: {h['content']}\n"

        prompt += f"\nUser: {transcript}\n"

        if rag_results:
            prompt += "\nAvailable products:\n"
            for p in rag_results.get("results", []):
                prompt += f"- {p['name']} | ₹{p['price']} | {p['category']}\n"

        prompt += "\nAssistant:"

        # 4️⃣ LLM
        reply_text = await self.llm.chat(prompt)
        reply_text = reply_text.strip()

        # 5️⃣ Save memory
        self.memory.add("user", transcript)
        self.memory.add("assistant", reply_text)

        # 6️⃣ Text → Speech (REAL AUDIO)
        try:
            audio_candidate = self.tts.synthesize(reply_text)
            if asyncio.iscoroutine(audio_candidate):
                reply_audio = await audio_candidate
            else:
                reply_audio = audio_candidate
        except Exception as e:
            print("TTS error:", repr(e))
            reply_audio = b""

        return {
            "user_transcript": transcript,
            "assistant_reply_text": reply_text,
            "assistant_reply_audio": reply_audio,
            "rag_results": rag_results,
        }
