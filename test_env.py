from dotenv import load_dotenv
import os

load_dotenv()

print("URL =", os.getenv("LIVEKIT_URL"))
print("KEY =", os.getenv("LIVEKIT_API_KEY"))
