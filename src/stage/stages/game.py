import utils
from utils import colorman
from stage import Stage


class GameStage(Stage):

    commands: dict[str, str] = {
        'help': 'print info about ? and ??',
        '?': 'list of available actions',
        '??': 'description of every command',
        'inv': 'open the inventory',
        'info': 'see vault\'s info',
        'exit': 'save a game and exit to menu'
    }

    def __init__(self, g):
        _name = 'Vault'
        super().__init__(_name, g)

    def loop(self) -> None:
        self.update_prompt()
        if self.game.kb.wait_for_enter():
            self.game.handle_command(self.game.kb.pop())

    def render(self, ts) -> None:
        utils.clear_screen() # NOTE if loop() will not be blocking anymore this will make screen blink
        padding: int = 3
        for component in self.game.components[::-1]:
            padding += len(component.texts)
            for i, text in enumerate(component.texts):
                utils.pprint(ts.lines-padding+i, 0, text)
        utils.pprint(ts.lines-2, 0, '┌'+'─'*(ts.columns-2)+'┐')
        utils.pprint(ts.lines, 0, '└'+'─'*(ts.columns-2)+'┘')
        utils.pprint(ts.lines-1, ts.columns, '│')
        utils.pprint(ts.lines-1, 0, '│ '+self.prompt)
        utils.fprint(colorman.CURSOR(len(self.raw_prompt)+3, ts.lines-1))


