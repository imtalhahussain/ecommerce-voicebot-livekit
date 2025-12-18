class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def last(self, n: int = 6):
        return self.history[-n:]
