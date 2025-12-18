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
from agent.llm import GroqAgent
from agent.models.edge_tts import EdgeTTS
from agent.config import LIVEKIT_URL
from agent.memory import ConversationMemory
from agent.intent import detect_intent, Intent
from agent.tools import search_products, track_order


TARGET_SR = 16000
CHANNELS = 1

# Speech detection
SPEECH_RMS = 900
SILENCE_FRAMES = 8
MIN_UTTERANCE_BYTES = TARGET_SR * 2  # ~1 second


def resample_48k_to_16k(pcm_48k: bytes) -> bytes:
    audio = np.frombuffer(pcm_48k, dtype=np.int16)
    return audio[::3].tobytes()


async def entrypoint(ctx: JobContext):
    print("🚀 Agent starting")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    print("🎤 Connected to room")

    # Publish agent audio
    audio_source = AudioSource(TARGET_SR, CHANNELS)
    agent_track = LocalAudioTrack.create_audio_track("agent-audio", audio_source)
    await ctx.room.local_participant.publish_track(agent_track)
    print("🔊 Agent audio track published")

    # Core components
    stt = WhisperSTT()
    llm = GroqAgent()
    tts = EdgeTTS()
    memory = ConversationMemory()

    agent_speaking = asyncio.Event()
    stop_tts = asyncio.Event()

    async def handle_audio(track):
        buffer_48k = bytearray()
        utterance_16k = bytearray()
        silence_count = 0
        in_speech = False

        async for event in AudioStream(track):
            if not hasattr(event, "frame"):
                continue

            frame: AudioFrame = event.frame
            buffer_48k.extend(frame.data)

            if len(buffer_48k) < 48000 * 2:
                continue

            pcm_48k = bytes(buffer_48k)
            buffer_48k.clear()

            pcm_16k = resample_48k_to_16k(pcm_48k)
            samples = np.frombuffer(pcm_16k, dtype=np.int16)
            rms = int(np.sqrt(np.mean(samples.astype(np.float32) ** 2)))
            print("🎚 RMS:", rms)

            # Barge-in
            if agent_speaking.is_set() and rms >= SPEECH_RMS:
                stop_tts.set()
                agent_speaking.clear()

            if rms >= SPEECH_RMS:
                in_speech = True
                silence_count = 0
                utterance_16k.extend(pcm_16k)
                continue

            if in_speech:
                silence_count += 1
                utterance_16k.extend(pcm_16k)

                if silence_count < SILENCE_FRAMES:
                    continue

                in_speech = False

                if len(utterance_16k) < MIN_UTTERANCE_BYTES:
                    utterance_16k.clear()
                    continue

                turn_start = time.perf_counter()

                # ---- STT ----
                stt_start = time.perf_counter()
                text = await stt.transcribe(bytes(utterance_16k))
                stt_time = (time.perf_counter() - stt_start) * 1000
                utterance_16k.clear()

                if not text:
                    continue

                print("🧠 STT:", text)
                memory.add_user(text)

                # ---- INTENT ----
                intent = detect_intent(text)
                print("🧭 Intent:", intent)

                # ---- TOOL ROUTING ----
                if intent == Intent.PRODUCT_SEARCH:
                    products = search_products(text)

                    narration_prompt = (
                        "You are a shopping assistant. "
                        "Explain the following products clearly and briefly, "
                        "based ONLY on this data:\n\n"
                        f"{products}"
                    )

                    reply = await llm.reply(narration_prompt, memory)

                elif intent == Intent.ORDER_TRACKING:
                    order = track_order("ORD123")

                    narration_prompt = (
                        "You are a customer support agent. "
                        "Explain the order status clearly using ONLY this data:\n\n"
                        f"{order}"
                    )

                    reply = await llm.reply(narration_prompt, memory)

                else:
                    reply = await llm.reply(text, memory)

                memory.add_assistant(reply)
                print("🤖 Reply:", reply)

                # ---- TTS ----
                agent_speaking.set()
                stop_tts.clear()

                tts_start = time.perf_counter()
                audio_bytes = await tts.synthesize(reply)
                tts_time = (time.perf_counter() - tts_start) * 1000

                samples_out = np.frombuffer(audio_bytes, dtype=np.int16)
                frame_size = 320  # 20ms

                for i in range(0, len(samples_out), frame_size):
                    if stop_tts.is_set():
                        break

                    chunk = samples_out[i:i + frame_size]
                    if len(chunk) < frame_size:
                        break

                    await audio_source.capture_frame(
                        AudioFrame(
                            data=chunk.tobytes(),
                            sample_rate=TARGET_SR,
                            num_channels=1,
                            samples_per_channel=frame_size,
                        )
                    )
                    await asyncio.sleep(0.02)

                # ---- Silence flush (important) ----
                silence = np.zeros(frame_size, dtype=np.int16)
                for _ in range(12):
                    await audio_source.capture_frame(
                        AudioFrame(
                            data=silence.tobytes(),
                            sample_rate=TARGET_SR,
                            num_channels=1,
                            samples_per_channel=frame_size,
                        )
                    )
                    await asyncio.sleep(0.02)

                agent_speaking.clear()

                total = (time.perf_counter() - turn_start) * 1000
                print(
                    f"\n📊 METRICS | STT {stt_time:.0f}ms | "
                    f"TTS {tts_time:.0f}ms | TOTAL {total:.0f}ms\n"
                )

    def attach(track):
        if track.kind == TrackKind.KIND_AUDIO:
            asyncio.create_task(handle_audio(track))

    @ctx.room.on("track_subscribed")
    def on_track(track, publication, participant):
        attach(track)

    for p in ctx.room.remote_participants.values():
        for pub in p.track_publications.values():
            if pub.track:
                attach(pub.track)

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("🛑 Agent shutdown")


def main():
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            ws_url=LIVEKIT_URL,
        )
    )


if __name__ == "__main__":
    main()
