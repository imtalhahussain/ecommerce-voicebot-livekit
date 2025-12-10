from __future__ import annotations

import asyncio
from dataclasses import dataclass

from dotenv import load_dotenv
load_dotenv()   # force-load .env manually

from .config import settings
from .models.stt import DummySpeechToText
from .models.llm import MockLLM
from .models.tts import DummyTextToSpeech
from .pipeline import VoicePipeline


@dataclass
class AgentContext:
    """Holds shared config and dependencies for the voice agent."""
    livekit_url: str | None
    livekit_api_key: str | None
    livekit_api_secret: str | None
    openai_api_key: str | None


def select_llm() -> MockLLM:
    """
    TEMP: Force MockLLM while we develop other system pieces.
    """
    print("TEMP: forcing Mock LLM (OpenAI disabled for now)")
    return MockLLM()


async def run_agent(context: AgentContext) -> None:
    """
    Main agent loop for testing Day 6 features:
    - Choose STT provider based on STT_PROVIDER env (.env): mock | whisper
    - Build pipeline and run either a file-based demo or LiveKit stub demo (if AUDIO_FILE set)
    """
    import os

    # read env (weforce load .env at top of file via load_dotenv())
    stt_provider = os.getenv("STT_PROVIDER", "mock").lower()
    audio_file = os.getenv("AUDIO_FILE")  # optional path to .wav file for demo
    livekit_simulate = os.getenv("USE_LIVEKIT_STUB", "false").lower() in ("1", "true", "yes")

    # Debug prints so we can see what the code reads from .env
    print("DEBUG env -> STT_PROVIDER:", stt_provider)
    print("DEBUG env -> USE_LIVEKIT_STUB:", os.getenv("USE_LIVEKIT_STUB"))
    print("DEBUG env -> AUDIO_FILE:", audio_file)

    # Build selected STT
    from .models.stt import build_stt
    try:
        if stt_provider == "whisper":
            print("Using LocalWhisperSTT (requires openai-whisper & ffmpeg).")
            stt_impl = build_stt("whisper")
        else:
            print("Using DummySpeechToText (mock).")
            stt_impl = build_stt("mock")
    except Exception as e:
        print("Failed to initialize selected STT provider:", e)
        print("Falling back to DummySpeechToText.")
        stt_impl = build_stt("mock")

    pipeline = VoicePipeline(
        stt=stt_impl,
        llm=select_llm(),
        tts=DummyTextToSpeech(),
    )

    print("=== Ecommerce Voice Agent (Day 6 test) ===")
    print(f"LiveKit URL: {context.livekit_url or '[not set]'}")

    # If user asked to simulate LiveKit, run the LiveKit stub
    if livekit_simulate and audio_file:
        from .livekit_stub import LiveKitStub
        stub = LiveKitStub()
        print(f"[LiveKit] Starting LiveKit stub simulation with file: {audio_file}")
        result = await stub.run_demo(audio_file, pipeline.handle_audio_turn)
    else:
        # if audio_file provided, run a one-shot file demo through pipeline
        if audio_file:
            print(f"Running single-file STT demo using: {audio_file}")
            from pathlib import Path
            p = Path(audio_file)
            if not p.exists():
                print("Audio file not found, running fake audio turn instead.")
                fake_audio = b"FAKE_AUDIO_FROM_USER_STREAM"
                result = await pipeline.handle_audio_turn(fake_audio)
            else:
                audio_bytes = p.read_bytes()
                result = await pipeline.handle_audio_turn(audio_bytes)
        else:
            # default: the same fake audio as before
            fake_audio = b"FAKE_AUDIO_FROM_USER_STREAM"
            result = await pipeline.handle_audio_turn(fake_audio)

    print("\n--- Pipeline Result ---")
    print(f"User transcript: {result['user_transcript']}")
    print(f"Assistant reply text: {result['assistant_reply_text']}")
    print(f"Assistant reply audio bytes length: {len(result['assistant_reply_audio'])}")
    print("-----------------------")
    print("TODO: connect this pipeline to real LiveKit for realtime streaming.")


def main() -> None:
    context = AgentContext(
        livekit_url=settings.livekit_url,
        livekit_api_key=settings.livekit_api_key,
        livekit_api_secret=settings.livekit_api_secret,
        openai_api_key=settings.openai_api_key,
    )

    asyncio.run(run_agent(context))


if __name__ == "__main__":
    main()
