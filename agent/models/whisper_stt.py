import numpy as np
from faster_whisper import WhisperModel
from livekit.rtc import AudioFrame


class WhisperSpeechToText:
    def __init__(self):
        self.model = WhisperModel("base", compute_type="int8")

    async def transcribe(self, frame: AudioFrame) -> str:
        # PCM int16 → numpy
        pcm = np.frombuffer(frame.data, dtype=np.int16)

        # int16 → float32 [-1, 1]
        audio = pcm.astype(np.float32) / 32768.0

        segments, _ = self.model.transcribe(
            audio,
            language="en",
            vad_filter=False,
            beam_size=5,
            temperature=0.0,
            log_prob_threshold=-5.0,
            no_speech_threshold=0.1,
            compression_ratio_threshold=5.0,
            condition_on_previous_text=False,
        )

        return " ".join(seg.text for seg in segments).strip()
