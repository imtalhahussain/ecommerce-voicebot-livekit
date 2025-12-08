"""
Entry point for the LiveKit-based ecommerce voice agent.

Day 2 goal:
- Prepare a clean structure for connecting to LiveKit
- Add a simple event loop placeholder that we can later extend
  with STT -> LLM -> TTS and ecommerce tools.
"""

import asyncio
from dataclasses import dataclass

from config import settings


@dataclass
class AgentContext:
    """Holds shared config and dependencies for the voice agent."""
    livekit_url: str | None
    livekit_api_key: str | None
    livekit_api_secret: str | None
    openai_api_key: str | None


async def run_agent(context: AgentContext) -> None:
    """
    Main agent loop.

    In later days, this will:
    - Connect to LiveKit
    - Listen for incoming audio sessions
    - Run STT -> LLM -> TTS pipeline
    - Call tools for product search and order tracking
    """

    # For now, just log what would happen.
    print("=== Ecommerce Voice Agent (Day 2 skeleton) ===")
    print(f"LiveKit URL: {context.livekit_url or '[not set]'}")
    print(f"OpenAI key configured: {bool(context.openai_api_key)}")
    print("TODO: connect to LiveKit, handle sessions, stream audio.")
    await asyncio.sleep(0.1)  # just so it's a proper async function


def main() -> None:
    context = AgentContext(
        livekit_url=settings.livekit_url,
        livekit_api_key=settings.livekit_api_key,
        livekit_api_secret=settings.livekit_api_secret,
        openai_api_key=settings.openai_api_key,
    )

    asyncio.run(run_agent(context))


if __name__ == "__main__":
    main()
