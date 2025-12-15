# agent/models/whisper_stt.py

import whisper
import asyncio
import tempfile
import os

class WhisperSpeechToText:
    def __init__(self, model_size="base"):
        print("Using Whisper STT")
        self.model = whisper.load_model(model_size)

    async def transcribe(self, audio_bytes: bytes) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            result = await asyncio.to_thread(
                self.model.transcribe,
                tmp_path,
                language="en",
                fp16=False
            )

            text = result.get("text", "").strip()
            print(f"[Whisper DEBUG] Transcript = '{text}'")

            return text

        finally:
            os.remove(tmp_path)
