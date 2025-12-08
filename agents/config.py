from pydantic_settings import BaseSettings

class AgentSettings(BaseSettings):
    # LiveKit connection
    livekit_url: str | None = None
    livekit_api_key: str | None = None
    livekit_api_secret: str | None = None

    # LLM / AI providers
    openai_api_key: str | None = None

    # Future: STT / TTS configs can go here

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = AgentSettings()
