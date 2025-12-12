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
        """
        Orchestrate one audio turn:
         - STT (awaited)
         - optional RAG call (awaited)
         - LLM chat (awaited)
         - TTS synth (sync or async handled)
        Returns a dict with transcript, reply text, reply audio bytes and rag_results.
        """
        # 1) STT: transcribe (await because implementations may be async)
        try:
            transcript = await self.stt.transcribe(audio_bytes)
        except TypeError:
            # fallback if an older STT implementation is synchronous
            transcript = self.stt.transcribe(audio_bytes)

        # Ensure transcript is a string
        if asyncio.iscoroutine(transcript):
            transcript = await transcript
        transcript = (transcript or "").strip()

        rag_results = None

        # 2) Intent detection and RAG call (if product question)
        if transcript and is_product_query(transcript):
            try:
                rag_results = await self.rag_tool.run(transcript)
            except Exception as e:
                print("RAG tool error:", repr(e))
                rag_results = None

        # 3) Build prompt for LLM
        prompt = f"User said: {transcript}\n"
        if rag_results:
            prompt += "\nMatching products (from RAG):\n"
            # format results compactly for the LLM prompt
            for p in rag_results.get("results", rag_results if isinstance(rag_results, list) else []):
                # handle both list-of-dicts or backend dict format
                if isinstance(p, dict):
                    prompt += f"- {p.get('name')} | {p.get('category')} | ₹{p.get('price')}\n"
                else:
                    prompt += f"- {p}\n"
        else:
            prompt += "\nNo product matches or not a product query.\n"

        # 4) Call LLM (await — your MockLLM/OpenAILLM should support async)
        try:
            reply_text = await self.llm.chat(prompt)
        except TypeError:
            # if llm.chat is sync, run in thread
            reply_text = await asyncio.to_thread(self.llm.chat, prompt)

        reply_text = (reply_text or "").strip()

        # 5) TTS: may be sync or async. Try await first, else run in thread.
        reply_audio = b""
        try:
            # some TTS implementations provide async synthesize
            reply_audio_candidate = self.tts.synthesize(reply_text)
            if asyncio.iscoroutine(reply_audio_candidate):
                reply_audio = await reply_audio_candidate
            else:
                # sync result (bytes) - ensure it's bytes
                reply_audio = reply_audio_candidate
        except TypeError:
            # fallback: run potentially blocking synth in thread
            reply_audio = await asyncio.to_thread(self.tts.synthesize, reply_text)
        except Exception as e:
            print("TTS error:", repr(e))
            reply_audio = b""

        return {
            "user_transcript": transcript,
            "assistant_reply_text": reply_text,
            "assistant_reply_audio": reply_audio,
            "rag_results": rag_results,
        }
