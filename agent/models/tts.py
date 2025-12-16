import pyttsx3
import io
import wave

class FemaleTextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()

        # Select female voice if available
        voices = self.engine.getProperty("voices")
        for v in voices:
            if "female" in v.name.lower() or "zira" in v.name.lower():
                self.engine.setProperty("voice", v.id)
                break

        self.engine.setProperty("rate", 165)

    def synthesize(self, text: str) -> bytes:
        buffer = io.BytesIO()

        def save_audio():
            self.engine.save_to_file(text, "temp_tts.wav")
            self.engine.runAndWait()

        save_audio()

        with wave.open("temp_tts.wav", "rb") as wf:
            buffer.write(wf.readframes(wf.getnframes()))

        return buffer.getvalue()
