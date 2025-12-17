print("RUNNING FILE:", __file__)

from dotenv import load_dotenv
load_dotenv()

import asyncio
import numpy as np

from livekit.agents import JobContext, WorkerOptions, cli, AutoSubscribe
from livekit.rtc import (
    AudioSource,
    LocalAudioTrack,
    AudioFrame,
    TrackKind,
    AudioStream,
)

# ✅ YOUR EXISTING MODELS (DO NOT CHANGE THEM)
from agent.models.whisper_stt import WhisperSpeechToText
from agent.models.edge_tts import TextToSpeech



async def entrypoint(ctx: JobContext):
    print("🔊 LiveKit agent connected")

    # Subscribe only to audio
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    print("✅ Room connected")
    print("👥 Local participant:", ctx.room.local_participant.identity)

    # STT & TTS
    stt = WhisperSpeechToText()
    tts = TextToSpeech()

    # Agent audio output
    audio_source = AudioSource(sample_rate=16000, num_channels=1)
    agent_track = LocalAudioTrack.create_audio_track(
        "agent-audio",
        audio_source,
    )

    await ctx.room.local_participant.publish_track(agent_track)
    print("🔊 Agent audio track published")

    # Kickstart audio stream (important for some browsers)
    silence = np.zeros(1600, dtype=np.int16)
    await audio_source.capture_frame(
        AudioFrame(
            data=silence.tobytes(),
            sample_rate=16000,
            num_channels=1,
            samples_per_channel=len(silence),
        )
    )

    async def handle_audio(track):
        print("🎧 Audio handler started")

        audio_stream = AudioStream(track)

        # 🔑 BUFFER SETTINGS (CRITICAL)
        buffer = bytearray()
        SAMPLE_RATE = 16000
        BYTES_PER_SAMPLE = 2  # int16
        TARGET_SECONDS = 1.0  # Whisper needs ~1s chunks

        TARGET_BYTES = int(SAMPLE_RATE * BYTES_PER_SAMPLE * TARGET_SECONDS)

        async for event in audio_stream:
            frame = event.frame

            # Accumulate raw PCM
            buffer.extend(frame.data)

            # Not enough audio yet
            if len(buffer) < TARGET_BYTES:
                continue

            # Build a single AudioFrame for Whisper
            audio_frame = AudioFrame(
                data=bytes(buffer),
                sample_rate=16000,
                num_channels=1,
                samples_per_channel=len(buffer) // 2,
            )

            buffer.clear()  # reset buffer

            try:
                text = await stt.transcribe(audio_frame)
                if not text:
                    continue

                print("🗣️ User:", text)

                reply = "Yes, I can hear you. How can I help you?"
                audio = await tts.synthesize(reply)

                pcm = np.frombuffer(audio, dtype=np.int16)
                await audio_source.capture_frame(
                    AudioFrame(
                        data=pcm.tobytes(),
                        sample_rate=16000,
                        num_channels=1,
                        samples_per_channel=len(pcm),
                    )
                )

                print("🔊 Agent spoke")

            except Exception as e:
                print("❌ Audio pipeline error:", e)

    # Subscribe to microphone tracks
    @ctx.room.on("track_subscribed")
    def on_track_subscribed(track, publication, participant):
        if track.kind == TrackKind.KIND_AUDIO:
            print("🎤 Microphone subscribed from:", participant.identity)
            asyncio.create_task(handle_audio(track))


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="voicebot",
        )
    )
