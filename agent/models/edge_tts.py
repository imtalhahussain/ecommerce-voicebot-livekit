import asyncio
import io
from pydub import AudioSegment
import edge_tts


class EdgeTTS:
    def __init__(self, voice="en-IN-NeerjaNeural"):
        self.voice = voice

    async def synthesize(self, text: str) -> bytes:
        """
        Returns raw PCM16 LE @ 16kHz mono
        """
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

        # ---- DECODE MP3 → PCM16 ----
        audio = AudioSegment.from_file(
            io.BytesIO(audio_bytes), format="mp3"
        )

        audio = (
            audio
            .set_frame_rate(16000)
            .set_channels(1)
            .set_sample_width(2)  # int16
        )

        return audio.raw_data
