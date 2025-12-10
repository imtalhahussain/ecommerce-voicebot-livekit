from __future__ import annotations

from abc import ABC, abstractmethod


class TextToSpeech(ABC):
    """Abstract interface for text-to-speech engines."""

    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """
        Convert a text response into audio bytes that can be streamed to
        the user via LiveKit.
        """
        raise NotImplementedError


class DummyTextToSpeech(TextToSpeech):
    """
    Dummy TTS implementation.

    Returns placeholder bytes so we can test the pipeline without
    integrating a real TTS provider yet.
    """

    async def synthesize(self, text: str) -> bytes:
        # Just encode the text as bytes for now. In reality, this would be
        # encoded audio (e.g., PCM / Opus).
        return text.encode("utf-8")
