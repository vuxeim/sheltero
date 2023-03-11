import os


import utils
from utils import colorman
import game
import command


class Stage():

    commands: dict = dict()

    def __init__(self, name: str, g):
        self.game: game.Game = g
        self.name: str = name
        self.prompt: str = str()
        self.raw_prompt: str = str()
        self.prompt_items: list[str] = list()
        self.command_handler: command.CommandHandler = command.CommandHandlerFactory(self.game, self)

    def loop(self) -> None:
        self.game.logger.error(f'Loop not inplemented for stage {self.name!r}')
        exit(1)

    def render(self, ts):
        self.game.logger.error(f'Rendering is not inplemented for stage {self.name!r}')
        exit(1)
    
    def show_credits(self):
        self.game.logger.error(f'Displaying credits is not implemented for stage {self.name!r}')
        exit(1)
    
    def close(self):
        self.game.logger.error(f'Closing is not implemented for stage {self.name!r}')
        exit(1)

    def update_prompt(self) -> None:
        final_items: list = []
        raw_items: list = []
        for item in self.prompt_items:
            if item in utils.colors.keys():
                _code = '\x1b[' + str(utils.colors[item]) + 'm'
                final_items.append(_code)
            elif item == 'stage':
                raw_items.append(self.name)
                final_items.append(self.name)
            elif len(item) == 1:
                raw_items.append(item)
                final_items.append(item)
            elif item == '':
                raw_items.append(' ')
                final_items.append(' ')
            else:
                raw_items.append(str(self.game.vault.data[item]))
                final_items.append(str(self.game.vault.data[item]))
        self.prompt: str = ''.join(final_items)
        self.raw_prompt: str = ''.join(raw_items)


class MainMenu(Stage):

    commands: dict[str, str] = {
        'l': 'load an existing save',
        'n': 'create a new save',
        'h': 'print some information',
        'e': 'exits the program'
    }

    def __init__(self, game):
        _name = 'Main Menu'
        super().__init__(_name, game)

    def loop(self) -> None:
        if self.game.kb.wait_for_input():
            self.game.kb.echo = True
            _cmd = self.game.kb.pop()
            self.game.handle_command(_cmd)

    def render(self, ts):
        utils.clear_screen()
        # Center text
        for component in self.game.components:
            padding: int = round(ts.lines*(2/3))-len(component.texts)//2
            for i, text in enumerate(component.texts):
                utils.pprint(padding+i, ts.columns//2-len(text)//2, text)

        # Sheltero title
        title: str = (' '*(ts.columns//20)).join('sheltero')
        utils.pprint(ts.lines//5, ts.columns//2-len(title)//2, title)

        # Email
        email: str = 'vuxeim@pm.me'
        utils.pprint(ts.lines//3-1, ts.columns-(len(email)+1), email)

        ## BORDERS
        # 1/3 border
        utils.pprint(ts.lines//3, 0, '#'*ts.columns)
        # Top border
        utils.pprint(0, 0, '#'*ts.columns)
        # Bottom border
        utils.pprint(ts.lines, 0, '#'*ts.columns)
        for line in range(ts.lines):
            # Left border
            utils.pprint(line, 0, '#')
            # Right border
            utils.pprint(line, ts.columns, '#')

    def show_credits(self) -> None:
        """ Displays short information about the game """
        _path: str = os.path.join(self.game.path, 'resources', 'texts', 'credits.txt')
        if os.path.exists(_path):
            with open(_path, 'r') as f:
                while (line := f.readline()):
                    print(line, end='')
        else:
            self.game.logger.warning(f'Unable to display credits. {_path} doesn\'t exist')


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


class Inventory(Stage):

    commands: dict[str, str] = {
        'help': '',
        '?': '',
        '??': '',
        'close': 'closes the inventory'
    }

    def __init__(self, g):
        super().__init__('Inventory', g)

    def loop(self) -> None:
        self.update_prompt()
        if self.game.kb.wait_for_enter():
            self.game.handle_command(self.game.kb.pop())

    def render(self, ts):
        utils.clear_screen()

    def close(self) -> None:
        utils.bprint('Inventory has been closed!')
        self.game.stages.pop()
