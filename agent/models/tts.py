import edge_tts

class TextToSpeech:
    def __init__(self):
        self.voice = "en-IN-NeerjaNeural"

    async def synthesize(self, text: str) -> bytes:
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            output_format="raw-16khz-16bit-mono-pcm"  # 🔴 REQUIRED
        )

        audio = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio += chunk["data"]

        return audio
