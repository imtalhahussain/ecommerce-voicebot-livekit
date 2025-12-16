from pydantic_settings import BaseSettings

class AgentSettings(BaseSettings):
    # LiveKit (future use)
    livekit_url: str | None = None
    livekit_api_key: str | None = None
    livekit_api_secret: str | None = None

    # OpenAI (future)
    openai_api_key: str | None = None

    # STT
    stt_provider: str = "mock"

    # Audio testing
    audio_file: str | None = None
    use_livekit_stub: bool = False

    # ElevenLabs
    elevenlabs_api_key: str | None = None
    elevenlabs_voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    class Config:
        env_file = ".env"
        extra = "ignore"   

settings = AgentSettings()
