import asyncio
from pathlib import Path

from agent.models.whisper_stt import WhisperSpeechToText
from agent.models.edge_tts import EdgeTextToSpeech
from agent.models.llm import MockLLM
from agent.pipeline import VoicePipeline

AUDIO_FILE = "audio/test_final.wav"

async def main():
    print("=== Ecommerce Voice Agent (Day 11 – Female TTS Test) ===")

    # STT
    stt = WhisperSpeechToText()

    # LLM (mock for now)
    llm = MockLLM()

    # Female TTS
    tts = EdgeTextToSpeech(voice="en-IN-NeerjaNeural")

    pipeline = VoicePipeline(stt=stt, llm=llm, tts=tts)

    audio_path = Path(AUDIO_FILE)
    audio_bytes = audio_path.read_bytes()

    result = await pipeline.handle_audio_turn(audio_bytes)

    # Save reply audio
    with open("reply.wav", "wb") as f:
        f.write(result["assistant_reply_audio"])

    print("User:", result["user_transcript"])
    print("Assistant:", result["assistant_reply_text"])
    print("Saved reply.wav (female voice)")

if __name__ == "__main__":
    asyncio.run(main())
