import asyncio
import numpy as np

from livekit.agents import JobContext, WorkerOptions, cli, AutoSubscribe
from livekit.rtc import AudioSource, LocalAudioTrack, AudioFrame
from agent.config import LIVEKIT_URL

SAMPLE_RATE = 48000
CHANNELS = 1

def generate_beep(duration_sec=1.0, freq=440):
    t = np.linspace(0, duration_sec, int(SAMPLE_RATE * duration_sec), False)
    tone = 0.3 * np.sin(2 * np.pi * freq * t)
    pcm = (tone * 32767).astype(np.int16)
    return pcm

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    print("Agent connected to room")

    audio_source = AudioSource(SAMPLE_RATE, CHANNELS)
    track = LocalAudioTrack.create_audio_track("agent-audio", audio_source)
    await ctx.room.local_participant.publish_track(track)

    # 🔊 PLAY TEST BEEP
    pcm = generate_beep()
    frame = AudioFrame(
        data=pcm.tobytes(),
        sample_rate=SAMPLE_RATE,
        num_channels=CHANNELS,
        samples_per_channel=len(pcm),
    )

    await audio_source.capture_frame(frame)
    print("Agent played test beep")

    while True:
        await asyncio.sleep(1)

def main():
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            ws_url=LIVEKIT_URL,
        )
    )

if __name__ == "__main__":
    main()
