import numpy as np
from faster_whisper import WhisperModel


class WhisperSTT:
    def __init__(self):
        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    async def transcribe(self, pcm_16k: bytes) -> str:
        """
        pcm_16k: raw 16-bit mono PCM @ 16kHz
        """

        # Convert bytes → float32 numpy array (REQUIRED)
        audio = np.frombuffer(pcm_16k, dtype=np.int16).astype(np.float32) / 32768.0

        segments, _ = self.model.transcribe(
            audio,
            language="en",
            beam_size=5,
        )

        text = "".join(seg.text for seg in segments).strip()
        return text
