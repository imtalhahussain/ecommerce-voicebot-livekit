from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from .config import settings
from .pipeline import VoicePipeline
from .models.stt import DummySpeechToText
from .models.llm import MockLLM
from .models.pyttsx3_tts import Pyttsx3TextToSpeech
from .models.whisper_stt import WhisperSpeechToText


@dataclass
class AgentContext:
    livekit_url: str | None
    livekit_api_key: str | None
    livekit_api_secret: str | None
    openai_api_key: str | None


def select_stt():
    if settings.stt_provider == "whisper":
        return WhisperSpeechToText()
    return DummySpeechToText()


def select_llm():
    print("TEMP: forcing Mock LLM (OpenAI disabled for now)")
    return MockLLM()


async def run_agent(context: AgentContext):
    print("=== Ecommerce Voice Agent (Day 10 test) ===")
    print(f"LiveKit URL: {context.livekit_url or '[not set]'}")

    pipeline = VoicePipeline(
        stt=select_stt(),
        llm=select_llm(),
        tts=Pyttsx3TextToSpeech(),
    )

    # 🔴 IMPORTANT CHANGE: read REAL audio file for Whisper
    if settings.stt_provider == "whisper":
        audio_path = Path(settings.audio_file)
        if not audio_path.exists():
            raise FileNotFoundError(f"AUDIO_FILE not found: {audio_path}")

        print(f"Reading audio file: {audio_path}")
        fake_audio = audio_path.read_bytes()
    else:
        fake_audio = b"FAKE_AUDIO_FROM_USER_STREAM"

    result = await pipeline.handle_audio_turn(fake_audio)

    print("\n--- Pipeline Result ---")
    print(f"User transcript: {result['user_transcript']}")
    print(f"Assistant reply text: {result['assistant_reply_text']}")
    print(f"Assistant reply audio bytes length: {len(result['assistant_reply_audio'])}")
    print("-----------------------")


def main():
    context = AgentContext(
        livekit_url=settings.livekit_url,
        livekit_api_key=settings.livekit_api_key,
        livekit_api_secret=settings.livekit_api_secret,
        openai_api_key=settings.openai_api_key,
    )

    asyncio.run(run_agent(context))


if __name__ == "__main__":
    main()
