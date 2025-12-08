# Voicebot Pipeline (v0)

1. User speaks into the web frontend (mic on browser).
2. Audio is streamed via LiveKit (WebRTC) to the Agent.
3. Agent:
   - Uses STT to convert speech → text.
   - Sends text to LLM with tools (product search, order tracking, FAQ).
   - Optionally uses RAG to fetch product / policy info.
   - Receives text response from LLM.
   - Converts text → speech using TTS.
4. Audio response is streamed back via LiveKit to the frontend.
5. Frontend also shows:
   - Live transcripts (user + bot)
   - Product cards returned by tools
   - Order status details
