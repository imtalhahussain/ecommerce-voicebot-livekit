# Ecommerce Voice Agent (LiveKit)

This folder contains the real-time voice agent that connects to LiveKit,
listens to user audio, and streams AI responses back.

Planned pipeline:

1. Connect to LiveKit server as an agent participant.
2. Receive audio from the frontend via WebRTC.
3. Run **STT → LLM → TTS**:
   - STT: transcribe user speech.
   - LLM: reason, call tools (product search, order tracking, FAQ).
   - TTS: synthesize a natural voice reply.
4. Stream the audio reply back to the frontend in real time.
5. Log transcripts, tool calls, and key metrics.

Day 2 status:
- Configuration via `AgentSettings` (LiveKit + OpenAI).
- Async `run_agent` loop placeholder prepared in `agent_main.py`.

## Current status (Day 3)

- Defined abstract interfaces for:
  - `SpeechToText`
  - `LLMClient`
  - `TextToSpeech`
- Implemented dummy / mock versions for early testing.
- Added `VoicePipeline` that runs a full STT -> LLM -> TTS turn.
- `agent_main.py` now constructs the pipeline and logs a sample result.
