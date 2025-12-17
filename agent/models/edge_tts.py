print("RUNNING FILE:", __file__)

import edge_tts


class TextToSpeech:
    def __init__(self, voice="en-IN-NeerjaNeural"):
        self.voice = voice

    async def synthesize(self, text: str) -> bytes:
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate="+0%",
            volume="+0%",
        )

        audio_bytes = bytearray()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes.extend(chunk["data"])

        return bytes(audio_bytes)
