from __future__ import annotations
import asyncio
from pathlib import Path
from typing import Callable

"""
LiveKit stub for local dev.

- simulate_audio(file_path, callback) reads a local wav file and calls `callback(audio_bytes)`
  to imitate incoming audio chunks. Example callback is VoicePipeline.handle_audio_turn.
- This is NOT production LiveKit — it's a local simulator to test pipeline + STT + TTS.
"""

class LiveKitStub:
    def __init__(self, chunk_ms: int = 150):
        self.chunk_ms = chunk_ms
        self._running = False

    async def simulate_audio_file(self, file_path: str, callback: Callable[[bytes], asyncio.Future]):
        """
        Read whole file and call callback once (or multiple times if you implement chunking).
        For Day 6 we call callback with full file bytes to keep things simple.
        """
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        audio_bytes = p.read_bytes()
        # In a real setup you'd stream chunks — here we just call once.
        print(f"[LiveKitStub] Simulating audio from {file_path} ({len(audio_bytes)} bytes)")
        return await callback(audio_bytes)

    async def run_demo(self, file_path: str, callback: Callable[[bytes], asyncio.Future]):
        """
        Convenience to run the demo: call simulate_audio_file and print.
        """
        self._running = True
        try:
            result = await self.simulate_audio_file(file_path, callback)
            return result
        finally:
            self._running = False
