from __future__ import annotations

from abc import ABC, abstractmethod


class SpeechToText(ABC):
    """Abstract interface for speech-to-text engines."""

    @abstractmethod
    async def transcribe(self, audio: bytes) -> str:
        """
        Convert raw audio bytes into a text transcript.

        In a real implementation, `audio` would be a chunk/stream from
        LiveKit. For Day 3 we just simulate this.
        """
        raise NotImplementedError


class DummySpeechToText(SpeechToText):
    """
    Dummy STT implementation used for early pipeline testing.

    Instead of actually decoding audio, it returns a fixed string so we can
    verify the pipeline and LLM/TTS layers.
    """

    async def transcribe(self, audio: bytes) -> str:
        # In later days, this will be replaced by a real STT engine.
        return "Hi, I want to buy running shoes under 3000 rupees."

def build_stt(provider: str = "mock", **kwargs):
    """
    Factory helper: provider: "mock" | "whisper"
    """
    if provider == "whisper":
        from .stt_whisper import LocalWhisperSTT
        return LocalWhisperSTT(**kwargs)
    # default mock
    from .stt import DummySpeechToText as _D
    return _D()