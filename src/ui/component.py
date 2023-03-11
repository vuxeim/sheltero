class UIComponent:

    def __init__(self, width: int = 20, height: int = 10):

        self.width = width
        self.height = height

    def render(self, *_):


        raise NotImplementedError('Rendering is not implemented for ' + __qualname__)


class CommandOutput(UIComponent):

    def __init__(self, *segments: str):
        self.texts = []
        for segment in segments:
            self.texts += segment.split('\n')


class MainMenu(UIComponent):

    def __init__(self, segments: list[str]):
        self.texts = segments

    def render(self, g):
        ...


class ConfirmationDialog(UIComponent):

    def __init__(self, message: str, width: int = 20, height: int = 10):
        super().__init__(width, height)
        self.message = message


class InputBox(UIComponent):

    ...
