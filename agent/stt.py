import numpy as np
from faster_whisper import WhisperModel


class WhisperSTT:
    def __init__(self):
        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )

    async def transcribe(self, pcm_bytes: bytes) -> str:
        """
        pcm_bytes: 16-bit PCM mono @ 16kHz
        """

        # Convert PCM16 → float32 [-1, 1]
        audio = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        segments, _ = self.model.transcribe(
            audio,
            language="en",
            vad_filter=True,
        )

        text = " ".join(seg.text.strip() for seg in segments)
        return text.strip()
