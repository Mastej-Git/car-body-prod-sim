class Place:
    def __init__(self, name, description="", tokens=0, max_tokens=1) -> None:
        self.name = name
        self.description = description
        self.tokens = tokens
        self.max_tokens = max_tokens

    def __str__(self) -> str:
        return f"Place({self.name}, tokens={self.tokens}, max_tokens={self.max_tokens})"
    