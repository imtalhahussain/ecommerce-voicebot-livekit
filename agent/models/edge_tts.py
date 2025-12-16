import edge_tts
import asyncio
import tempfile
import os

class EdgeTextToSpeech:
    def __init__(self, voice: str = "en-IN-NeerjaNeural"):
        # Female Indian English voice
        self.voice = voice

    async def synthesize(self, text: str) -> bytes:
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate="+0%",
            volume="+0%"
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            path = tmp.name

        await communicate.save(path)

        with open(path, "rb") as f:
            audio = f.read()

        os.remove(path)
        return audio
