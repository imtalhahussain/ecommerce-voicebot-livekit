from collections import deque

class ConversationMemory:
    def __init__(self, max_turns: int = 6):
        self.messages = deque(maxlen=max_turns * 2)

    def add_user(self, text: str):
        self.messages.append({
            "role": "user",
            "parts": [{"text": text}]
        })

    def add_assistant(self, text: str):
        self.messages.append({
            "role": "model",
            "parts": [{"text": text}]
        })

    def last(self, n: int):
        return list(self.messages)[-n:]
