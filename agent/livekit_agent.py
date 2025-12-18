import asyncio
import time
import numpy as np

from livekit.agents import JobContext, WorkerOptions, cli, AutoSubscribe
from livekit.rtc import (
    AudioSource,
    LocalAudioTrack,
    AudioFrame,
    AudioStream,
    TrackKind,
)

from agent.stt import WhisperSTT
from agent.llm import GeminiAgent
from agent.models.edge_tts import EdgeTTS
from agent.config import LIVEKIT_URL

# ========================
# AUDIO CONSTANTS
# ========================

TARGET_SR = 16000
CHANNELS = 1

VOICE_RMS_THRESHOLD = 1200     # definite speech
NOISE_FLOOR = 600              # anything below = silence
END_SILENCE_SECONDS = 0.7      # pause to end utterance
MIN_UTTERANCE_SECONDS = 0.8    # ignore very short noise

# ========================
# UTILS
# ========================

def resample_48k_to_16k(pcm_48k: bytes) -> bytes:
    audio = np.frombuffer(pcm_48k, dtype=np.int16).astype(np.float32)
    audio_16k = audio[::3]  # 48k → 16k
    return audio_16k.astype(np.int16).tobytes()


# ========================
# AGENT ENTRYPOINT
# ========================

async def entrypoint(ctx: JobContext):
    print("🚀 Agent starting")

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    print("🎤 Agent connected")

    # Agent audio output
    audio_source = AudioSource(TARGET_SR, CHANNELS)
    agent_track = LocalAudioTrack.create_audio_track("agent-audio", audio_source)
    await ctx.room.local_participant.publish_track(agent_track)
    print("🔊 Agent audio track published")

    stt = WhisperSTT()
    llm = GeminiAgent()
    tts = EdgeTTS()

    async def handle_audio(track):
        print("🔊 AudioStream started")

        buffer_48k = bytearray()
        utterance_buffer = bytearray()

        speaking = False
        utterance_start = 0.0
        last_voice_time = 0.0

        async for event in AudioStream(track):
            if not hasattr(event, "frame"):
                continue

            frame: AudioFrame = event.frame
            buffer_48k.extend(frame.data)

            # 1 second @ 48kHz mono
            if len(buffer_48k) < 48000 * 2:
                continue

            pcm_48k = bytes(buffer_48k)
            buffer_48k.clear()

            pcm_16k = resample_48k_to_16k(pcm_48k)
            samples = np.frombuffer(pcm_16k, dtype=np.int16)

            rms = int(np.sqrt(np.mean(samples.astype(np.float32) ** 2)))
            print("🎚 RMS:", rms)

            now = time.time()

            # -----------------------------
            # SPEECH DETECTION
            # -----------------------------
            if rms >= VOICE_RMS_THRESHOLD:
                if speaking and (now - utterance_start) > 6.0:
                    print("⏱ Max utterance length reached")
                    speaking = False

                if not speaking:
                    speaking = True
                    utterance_start = now
                    utterance_buffer.clear()
                    print("🟢 Speech started")

                last_voice_time = now
                utterance_buffer.extend(pcm_16k)
                continue

            # -----------------------------
            # SILENCE HANDLING
            # -----------------------------
            if speaking and rms < NOISE_FLOOR:
                if (now - last_voice_time) >= END_SILENCE_SECONDS:
                    duration = now - utterance_start
                    speaking = False

                    if duration < MIN_UTTERANCE_SECONDS:
                        print("🔇 Utterance too short, discarded")
                        utterance_buffer.clear()
                        continue

                    print("🧠 Sending utterance to STT...")
                    text = await stt.transcribe(bytes(utterance_buffer))
                    utterance_buffer.clear()

                    print("🧠 STT:", repr(text))
                    if not text:
                        continue

                    reply = f"You said {text}"
                    print("🤖 Reply:", reply)

                    # TTS output
                    audio_bytes = await tts.synthesize(reply)
                    out_samples = np.frombuffer(audio_bytes, dtype=np.int16)

                    frame_size = 320  # 20ms @ 16kHz
                    for i in range(0, len(out_samples), frame_size):
                        chunk = out_samples[i:i + frame_size]
                        if len(chunk) < frame_size:
                            break

                        out_frame = AudioFrame(
                            data=chunk.tobytes(),
                            sample_rate=TARGET_SR,
                            num_channels=1,
                            samples_per_channel=len(chunk),
                        )

                        await audio_source.capture_frame(out_frame)
                        await asyncio.sleep(0.02)

                    print("✅ Reply audio streamed")

    def attach(track):
        if track.kind == TrackKind.KIND_AUDIO:
            print("🔊 Subscribed to user audio track")
            asyncio.create_task(handle_audio(track))

    @ctx.room.on("track_subscribed")
    def on_track(track, publication, participant):
        attach(track)

    # Handle already existing tracks
    for p in ctx.room.remote_participants.values():
        for pub in p.track_publications.values():
            if pub.track:
                attach(pub.track)

    while True:
        await asyncio.sleep(1)


# ========================
# MAIN
# ========================

def main():
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            ws_url=LIVEKIT_URL,
        )
    )


if __name__ == "__main__":
    main()
