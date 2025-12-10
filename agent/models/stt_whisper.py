# Placeholder for Whisper STT (real implementation added later)
from __future__ import annotations

from .stt import SpeechToText

class LocalWhisperSTT(SpeechToText):
    async def transcribe(self, audio: bytes) -> str:
        return "Whisper STT not implemented yet"
