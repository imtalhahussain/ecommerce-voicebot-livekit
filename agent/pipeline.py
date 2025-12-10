from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from .models.stt import SpeechToText
from .models.llm import LLMClient
from .models.tts import TextToSpeech


@dataclass
class VoicePipeline:
    """
    End-to-end voice pipeline:

    audio (bytes) -> STT -> text -> LLM -> reply text -> TTS -> reply audio (bytes)
    """

    stt: SpeechToText
    llm: LLMClient
    tts: TextToSpeech

    async def handle_audio_turn(self, audio: bytes) -> Dict[str, Any]:
        """
        Process a single turn from user audio to bot audio reply.

        In a real-time LiveKit setup, this would work on streams/chunks
        instead of a single `audio` blob.
        """
        # 1) Audio -> text
        user_text = await self.stt.transcribe(audio)

        # 2) Text -> LLM reply text
        reply_text = await self.llm.chat(user_text)

        # 3) Reply text -> audio bytes
        reply_audio = await self.tts.synthesize(reply_text)

        return {
            "user_transcript": user_text,
            "assistant_reply_text": reply_text,
            "assistant_reply_audio": reply_audio,
        }
