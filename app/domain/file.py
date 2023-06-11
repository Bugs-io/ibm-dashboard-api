class File:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self.content = content

    def tuple(self):
        return (self.name, self.content)
