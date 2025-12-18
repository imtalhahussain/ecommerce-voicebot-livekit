import edge_tts

class EdgeTTS:
    def __init__(self, voice="en-IN-NeerjaNeural"):
        self.voice = voice

    async def synthesize(self, text: str) -> bytes:
        communicate = edge_tts.Communicate(text=text, voice=self.voice)

        audio = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio += chunk["data"]

        return audio
