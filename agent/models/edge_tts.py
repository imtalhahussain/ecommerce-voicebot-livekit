import edge_tts
import io
from pydub import AudioSegment

class EdgeTTS:
    def __init__(self, voice="en-IN-NeerjaNeural"):
        self.voice = voice

    async def synthesize(self, text: str) -> bytes:
        communicate = edge_tts.Communicate(text, self.voice)
        mp3 = io.BytesIO()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                mp3.write(chunk["data"])

        mp3.seek(0)
        audio = AudioSegment.from_mp3(mp3)
        audio = audio.set_frame_rate(16000).set_channels(1)
        return audio.raw_data
