"""
Centralized configuration for the voice agent.
"""

from pydantic import BaseSettings


class AgentSettings(BaseSettings):
    livekit_url: str | None = None
    livekit_api_key: str | None = None
    livekit_api_secret: str | None = None

    openai_api_key: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = AgentSettings()
