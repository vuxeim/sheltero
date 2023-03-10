class TextComponent: ...

class CommandOutput(TextComponent):
    def __init__(self, *segments: str):
        self.texts = []
        for segment in segments:
            self.texts += segment.split('\n')

class GameMenu(TextComponent):
    def __init__(self, segments: list[str]):
        self.texts = segments
