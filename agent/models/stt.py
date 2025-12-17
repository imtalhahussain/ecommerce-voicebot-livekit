import numpy as np
from faster_whisper import WhisperModel
from livekit.rtc import AudioFrame


class SpeechToText:
    def __init__(self):
        self.model = WhisperModel("base", compute_type="int8")

    async def transcribe(self, frame: AudioFrame) -> str:
        # Convert PCM bytes → int16
        pcm = np.frombuffer(frame.data, dtype=np.int16)

        # int16 → float32 [-1, 1]
        audio = pcm.astype(np.float32) / 32768.0

        segments, _ = self.model.transcribe(
            audio,
            language="en",
            vad_filter=True,
        )

        return " ".join(seg.text for seg in segments).strip()
