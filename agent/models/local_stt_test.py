import numpy as np
from faster_whisper import WhisperModel
import soundfile as sf

AUDIO_PATH = "sample.wav"  # 16kHz mono recommended

def main():
    audio, sr = sf.read(AUDIO_PATH)
    if sr != 16000:
        raise ValueError(f"Expected 16kHz audio, got {sr}")

    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    model = WhisperModel("base", compute_type="int8")

    segments, _ = model.transcribe(
        audio,
        language="en",
        vad_filter=True,
    )

    text = " ".join(seg.text for seg in segments).strip()
    print("TRANSCRIPT:", text)

if __name__ == "__main__":
    main()
