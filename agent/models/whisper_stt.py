import numpy as np
from faster_whisper import WhisperModel
from livekit.rtc import AudioFrame

class WhisperSTT:
    def __init__(self):
        self.model = WhisperModel("base", compute_type="int8")

    async def transcribe(self, frame: AudioFrame) -> str:
        pcm = np.frombuffer(frame.data, dtype=np.int16)
        audio = pcm.astype(np.float32) / 32768.0
        segments, _ = self.model.transcribe(audio, language="en")
        return " ".join(s.text for s in segments).strip()
