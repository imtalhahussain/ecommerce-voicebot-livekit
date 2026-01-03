import asyncio
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
from agent.llm import GroqAgent
from agent.models.edge_tts import EdgeTTS
from agent.config import LIVEKIT_URL
from agent.memory import ConversationMemory


TARGET_SR = 16000
CHANNELS = 1

# ---- Speech detection tuning ----
SPEECH_RMS = 900
SILENCE_FRAMES = 8
MIN_UTTERANCE_BYTES = TARGET_SR * 2  # ~1 second


def resample_48k_to_16k(pcm_48k: bytes) -> bytes:
    audio = np.frombuffer(pcm_48k, dtype=np.int16)
    audio_16k = audio[::3]  # 48k → 16k
    return audio_16k.tobytes()


async def entrypoint(ctx: JobContext):
    print("🚀 Agent starting")

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    print("🎤 Agent connected")

    # ---- Publish agent audio ----
    audio_source = AudioSource(TARGET_SR, CHANNELS)
    agent_track = LocalAudioTrack.create_audio_track(
        "agent-audio", audio_source
    )
    await ctx.room.local_participant.publish_track(agent_track)
    print("🔊 Agent audio track published")

    # ---- Core components ----
    stt = WhisperSTT()
    llm = GroqAgent()
    tts = EdgeTTS()
    memory = ConversationMemory()

    # ---- State flags ----
    agent_speaking = asyncio.Event()
    stop_tts = asyncio.Event()

    async def handle_audio(track):
        print("🔊 AudioStream started")

        buffer_48k = bytearray()
        utterance_16k = bytearray()
        silence_count = 0
        in_speech = False

        async for event in AudioStream(track):
            if not hasattr(event, "frame"):
                continue

            frame: AudioFrame = event.frame
            buffer_48k.extend(frame.data)

            # wait for ~1 sec of 48k audio
            if len(buffer_48k) < 48000 * 2:
                continue

            pcm_48k = bytes(buffer_48k)
            buffer_48k.clear()

            pcm_16k = resample_48k_to_16k(pcm_48k)
            samples = np.frombuffer(pcm_16k, dtype=np.int16)

            rms = int(np.sqrt(np.mean(samples.astype(np.float32) ** 2)))
            print("🎚 RMS:", rms)

            # ---- BARGE-IN DETECTION ----
            if agent_speaking.is_set() and rms >= SPEECH_RMS:
                print("⛔ Barge-in detected — stopping agent speech")
                stop_tts.set()
                agent_speaking.clear()

            if rms >= SPEECH_RMS:
                if not in_speech:
                    print("🟢 Speech started")
                in_speech = True
                silence_count = 0
                utterance_16k.extend(pcm_16k)
                continue

            if in_speech:
                silence_count += 1
                utterance_16k.extend(pcm_16k)

                if silence_count >= SILENCE_FRAMES:
                    in_speech = False

                    if len(utterance_16k) >= MIN_UTTERANCE_BYTES:
                        print("🧠 Sending utterance to STT...")

                        text = await stt.transcribe(bytes(utterance_16k))
                        utterance_16k.clear()
                        silence_count = 0

                        print("🧠 STT:", repr(text))
                        if not text:
                            continue

                        # ---- Conversation memory ----
                        memory.add_user(text)

                        reply = await llm.reply(text, memory)
                        memory.add_assistant(reply)

                        print("🤖 Reply:", reply)

                        # ---- Speak with interrupt support ----
                        agent_speaking.set()
                        stop_tts.clear()

                        audio_bytes = await tts.synthesize(reply)
                        out_samples = np.frombuffer(
                            audio_bytes, dtype=np.int16
                        )

                        frame_size = 320  # 20ms @ 16kHz
                        for i in range(0, len(out_samples), frame_size):
                            if stop_tts.is_set():
                                print("🛑 TTS interrupted")
                                break

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

                        agent_speaking.clear()
                        print("✅ Reply audio streamed")

                    else:
                        utterance_16k.clear()

    def attach(track):
        if track.kind == TrackKind.KIND_AUDIO:
            print("🔊 Subscribed to user audio track")
            asyncio.create_task(handle_audio(track))

    @ctx.room.on("track_subscribed")
    def on_track(track, publication, participant):
        attach(track)

    # attach already published tracks
    for p in ctx.room.remote_participants.values():
        for pub in p.track_publications.values():
            if pub.track:
                attach(pub.track)

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("🛑 Agent shutting down cleanly")


def main():
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            ws_url=LIVEKIT_URL,
        )
    )


if __name__ == "__main__":
    main()
