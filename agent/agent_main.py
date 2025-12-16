import asyncio
from pathlib import Path

from agent.models.whisper_stt import WhisperSpeechToText
from agent.models.tts import FemaleTextToSpeech
from agent.models.llm import MockLLM
from agent.pipeline import VoicePipeline

AUDIO_FILE = "audio/test_final.wav"

async def main():
    print("=== Ecommerce Voice Agent (Day 11 – Female TTS Stable) ===")

    stt = WhisperSpeechToText()
    llm = MockLLM()
    tts = FemaleTextToSpeech()

    pipeline = VoicePipeline(stt=stt, llm=llm, tts=tts)

    audio_path = Path(AUDIO_FILE)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")

    audio_bytes = audio_path.read_bytes()

    result = await pipeline.handle_audio_turn(audio_bytes)

    print("Transcript:", result["user_transcript"])
    print("Reply:", result["assistant_reply_text"])

    with open("reply.wav", "wb") as f:
        f.write(result["assistant_reply_audio"])

    print("Saved female voice reply → reply.wav")

if __name__ == "__main__":
    asyncio.run(main())
