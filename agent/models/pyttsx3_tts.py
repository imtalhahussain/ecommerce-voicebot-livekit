import pyttsx3
import asyncio
import io
import wave

class Pyttsx3TextToSpeech:
    def __init__(self):
        print("Using pyttsx3 TTS")
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 165)

    def _speak_to_wav(self, text: str) -> bytes:
        buffer = io.BytesIO()

        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)

            self.engine.save_to_file(text, "temp_tts.wav")
            self.engine.runAndWait()

            with open("temp_tts.wav", "rb") as f:
                wf.writeframes(f.read())

        return buffer.getvalue()

    async def synthesize(self, text: str) -> bytes:
        return await asyncio.to_thread(self._speak_to_wav, text)
