# Architecture (v0 Draft)

## Components

- **Frontend**
  - Web client (Next.js/React) that connects to LiveKit via WebRTC.
  - Handles mic access, displays transcripts and results.

- **Voice Agent (LiveKit)**
  - Listens to user audio streams.
  - Uses STT to convert speech → text.
  - Uses an LLM to decide how to respond and which tools to call.
  - Uses TTS to send back natural speech.

- **Backend (FastAPI)**
  - Product search API.
  - Order tracking API.
  - RAG APIs for FAQ/policy retrieval.
  - Data access layer for DB / vector store.

- **Data & RAG**
  - Product catalog (structured data + embeddings).
  - FAQ / policies (documents + embeddings).

This is a first draft and will evolve as the implementation grows.
