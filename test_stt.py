import asyncio
from agent.models.stt import WhisperSpeechToText

async def main():
    with open("test.wav", "rb") as f:
        audio = f.read()

    stt = WhisperSpeechToText()
    text = await stt.transcribe(audio, 16000)
    print(text)

asyncio.run(main())
