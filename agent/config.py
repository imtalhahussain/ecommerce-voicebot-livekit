import os
from dotenv import load_dotenv

load_dotenv()

LIVEKIT_URL = os.environ["LIVEKIT_URL"]
LIVEKIT_API_KEY = os.environ["LIVEKIT_API_KEY"]
LIVEKIT_API_SECRET = os.environ["LIVEKIT_API_SECRET"]

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
