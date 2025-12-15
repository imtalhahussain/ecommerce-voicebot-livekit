class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, role, content):
        self.history.append({"role": role, "content": content})

    def get(self, limit=6):
        return self.history[-limit:]
