# agent/config.py
from __future__ import annotations
from typing import Optional
from pydantic_settings import BaseSettings


class AgentSettings(BaseSettings):
    # LiveKit connection
    livekit_url: Optional[str] = None
    livekit_api_key: Optional[str] = None
    livekit_api_secret: Optional[str] = None

    # LLM / AI providers
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.5

    # Backend / deployment
    backend_url: str = "http://127.0.0.1:8000"

    # STT / LiveKit demo toggles (strings in .env like "true"/"false" will be parsed)
    stt_provider: str = "mock"            # "mock" | "whisper" etc.
    use_livekit_stub: bool = False        # true/false
    audio_file: Optional[str] = None      # optional path to a demo WAV file

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # forbid unknown by default is pydantic behaviour; we're explicitly listing fields

# instantiate settings used by the agent
settings = AgentSettings()
