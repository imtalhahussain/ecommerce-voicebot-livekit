from collections import deque

class ConversationMemory:
    def __init__(self, max_turns=6):
        self.messages = deque(maxlen=max_turns * 2)

    def add_user(self, text):
        self.messages.append({"role": "user", "content": text})

    def add_assistant(self, text):
        self.messages.append({"role": "assistant", "content": text})

    def as_messages(self):
        return list(self.messages)
