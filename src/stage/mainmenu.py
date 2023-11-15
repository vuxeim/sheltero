import os

from handler import CommandHandler
from ui import component
import utils
from stage import Stage


class MainMenuStage(Stage):

    def __init__(self, game):
        super().__init__(game)
        self.command_handler = MainMenuCommandHandler(game, self)

    def loop(self) -> None:
        super().loop()
        if self.game.keyb.wait_for_input():
            self.game.keyb.echo = True
            _cmd = self.game.keyb.pop()
            self.game.handle_command(_cmd)

    def show_credits(self) -> None:
        """ Displays short information about the game """
        _path: str = os.path.join(self.game.path, 'resources', 'texts', 'credits.txt')
        if os.path.exists(_path):
            with open(_path, 'r') as f:
                while (line := f.readline()):
                    print(line, end='')


def load(handler: CommandHandler) -> None:
    """ When user choose to load an already existing vault """
    # TODO sorting saves by latest play date
    _path: str = os.path.join(handler.game.path, 'saves')
    vaults: set[str] = set(d for d in os.listdir(_path) if os.path.isdir(os.path.join(_path, d)))
    handler.stage.components.append(
        component.CommandOutput(
            *[f'List of all your vaults ({len(vaults)}):',
            '\n'.join([f'{i}. {f}' for i, f in enumerate(vaults, start=1)]),
            f'Choose a vault to play on:']
        )
    )
    name: str = ""
    if handler.game.keyb.wait_for_enter():
        name = handler.game.keyb.pop().strip()
    if name.isdigit():
        # Asign a number to every name and get name of corresponing number
        name: str = {i: name for i, name in enumerate(vaults, start=1)}.get(int(name), '')
    if name in vaults:
        handler.game.start(name)
    else:
        print('\nVault doesn\'t exist')


def new(handler: CommandHandler) -> None:
    utils.bprint('Pick a name for your vault: ', end='')
    name: str = ""
    if handler.game.keyb.wait_for_enter():
        name = handler.game.keyb.pop().strip()
    if name != '':
        handler.game.start(name)
    else:
        utils.bprint('Vault\'s name not specified.')


def settings(handler: CommandHandler) -> None:
    # TODO settings stage
    print('settings will be here in the future')


def _help(handler: CommandHandler) -> None:
    handler.stage.show_credits()


def _quit(handler: CommandHandler) -> None:
    handler.game.quit()


class MainMenuCommandHandler(CommandHandler):

    callbacks = {
        'l': load,
        'n': new,
        's': settings,
        'h': _help,
        'q': _quit
    }
