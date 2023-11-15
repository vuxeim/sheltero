from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game
import utils
from utils import colorman


class UIComponent:

    def __init__(self):

        self._alive: bool = True
        self.name = self.__class__.__name__

    def __bool__(self) -> bool:
        return self._alive

    def dispose(self):
        self._alive = False

    def render(self, game: Game) -> None:
        raise NotImplementedError(f"Rendering is not implemented for component '{self.name}'")


class TextBox(UIComponent):

    def __init__(self, segments: list[str]):
        super().__init__()
        self.texts = []
        for segment in segments:
            self.texts += segment.split('\n')

    def render(self, game: Game) -> None:
        size = game.size
        padding: int = round(size.lines*(2/3))-len(self.texts)//2
        for i, text in enumerate(self.texts):
            utils.pprint(size.columns//2-len(text)//2, padding+i, text)

class CommandOutput(UIComponent):

    def __init__(self, *segments: str):
        super().__init__()
        self.texts = []
        for segment in segments:
            self.texts += segment.split('\n')

    def render(self, game: Game):
        size = game.size
        padding: int = round(size.lines*(2/3))-len(self.texts)//2
        for i, text in enumerate(self.texts):
            utils.pprint(size.columns//2-len(text)//2, padding+i, text)

    def __render(self, game: Game) -> None:
        size = game.size
        padding: int = 3
        for i, text in enumerate(self.texts):
            utils.pprint(size.lines-padding+i, 0, text)
        utils.pprint(size.lines-2, 0, '┌'+'─'*(size.columns-2)+'┐')
        utils.pprint(size.lines, 0, '└'+'─'*(size.columns-2)+'┘')
        utils.pprint(size.lines-1, size.columns, '│')
        utils.pprint(size.lines-1, 0, '│ '+game.stages.top().prompt)
        utils.fprint(colorman.CURSOR(len(game.stages.top().raw_prompt)+3, size.lines-1))

class MainMenu(UIComponent):

    def __init__(self):
        super().__init__()

    def render(self, game: Game):
        size = game.size

        # Sheltero title
        title: str = (' '*(size.columns//20)).join('sheltero')
        x, y = size.columns//2-len(title)//2, size.lines//5
        utils.pprint(x, y, title)

        # Email
        email: str = 'vuxeim@pm.me'
        x, y = size.columns-(len(email)+1), size.lines//3-1
        utils.pprint(x, y, email)
        return

        ## BORDERS
        # 1/3 border
        utils.pprint(0, size.lines//3, '#'*size.columns)
        # Top border
        utils.pprint(0, 0, '#'*size.columns)
        # Bottom border
        utils.pprint(0, size.lines, '#'*size.columns)
        for line in range(size.lines):
            # Left border
            utils.pprint(0, line, '#')
            # Right border
            utils.pprint(size.columns, line, '#')


class CommandInput(UIComponent):
    pass

class ConfirmationDialog(UIComponent):

    def __init__(self, message: str):
        super().__init__()
        self.message = message
