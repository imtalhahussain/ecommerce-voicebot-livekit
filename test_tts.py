import asyncio
from agent.models.tts import TextToSpeech

async def main():
    tts = TextToSpeech()
    audio = await tts.synthesize("Hello, this is a test")

    with open("out.pcm", "wb") as f:
        f.write(audio)

asyncio.run(main())
