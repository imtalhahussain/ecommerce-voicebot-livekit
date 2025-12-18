import numpy as np
from faster_whisper import WhisperModel

class WhisperSTT:
    def __init__(self):
        self.model = WhisperModel("base", compute_type="int8")

    async def transcribe(self, pcm_bytes: bytes) -> str:
        pcm = np.frombuffer(pcm_bytes, dtype=np.int16)
        audio = pcm.astype(np.float32) / 32768.0

        segments, _ = self.model.transcribe(
            audio,
            language="en",
            vad_filter=True,
        )
        return " ".join(s.text for s in segments).strip()
