class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def recent(self, limit: int = 6):
        return self.history[-limit:]
