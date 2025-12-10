from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import asyncio
import os

from openai import OpenAI
from ..config import settings


class LLMClient(ABC):
    @abstractmethod
    async def chat(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        raise NotImplementedError


class MockLLM(LLMClient):
    async def chat(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        return "This is a mock reply because OpenAI is not configured or is failing."


class OpenAILLM(LLMClient):
    def __init__(self) -> None:
        # 1️⃣ Read key from settings (.env) and also from OS, just to debug
        key_from_settings = settings.openai_api_key
        key_from_env = os.getenv("OPENAI_API_KEY")

        print("DEBUG key_from_settings prefix:", key_from_settings[:15] if key_from_settings else None)
        print("DEBUG key_from_env      prefix:", key_from_env[:15] if key_from_env else None)

        # 2️⃣ Decide which key to actually use
        key = key_from_settings or key_from_env
        if not key:
            raise ValueError("No OpenAI API key found in settings or environment.")

        print("DEBUG ACTUAL KEY USED prefix:", key[:15])

        # 3️⃣ Create client WITH the key explicitly (this bypasses implicit env usage)
        self.client = OpenAI(api_key=key)

    async def chat(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        def _call_openai() -> str:
            resp = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an ecommerce voice assistant."},
                    {"role": "user", "content": user_message},
                ],
            )
            return resp.choices[0].message.content

        return await asyncio.to_thread(_call_openai)
