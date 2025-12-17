import edge_tts

class TextToSpeech:
    def __init__(self, voice="en-IN-NeerjaNeural"):
        self.voice = voice

    async def synthesize(self, text: str) -> bytes:
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            output_format="raw-16khz-16bit-mono-pcm",
        )

        audio = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])

        return bytes(audio)
