import os

from keyboard import key as keycode
from ui import component
import utils
from stage import Stage


class MainMenuStage(Stage):

    def __init__(self, game):
        def is_name(name: str) -> bool:
            return os.path.isdir(os.path.join(self._path, name))
        super().__init__(game)
        self._name: str = ""
        self._path: str = os.path.join(self.game.path, 'saves')
        self._vaults: list[str] = list(filter(is_name, os.listdir(self._path)))

    def loop(self) -> None:
        super().loop()

        self._name = self.game.keyb.collect()
        if self._name is not None:
            self.cb_load_vault(self._name.strip())

        for key in (keycode.L, keycode.N, keycode.S, keycode.H, keycode.Q):
            if self.game.keyb.is_pressed(key):
                self.handle(key)
                self.game.keyb.echo = True

    def show_credits(self) -> None:
        # TODO: ditch print(), use ui components
        """ Displays short information about the game """
        _path: str = os.path.join(self.game.path, 'resources', 'texts', 'credits.txt')
        if os.path.exists(_path):
            with open(_path, 'r') as f:
                while (line := f.readline()):
                    print(line, end='')

    def close(self) -> None:
        pass

    def handle(self, inp: str) -> None:
        cb = {'l': self.cb_ask_for_vault,
              'n': self.cb_new,
              's': self.cb_settings,
              'h': self.cb_help,
              'q': self.cb_quit
              }.get(inp)
        if cb is not None:
            cb()

    def cb_load_vault(self, name: str) -> None:
        if name.isdigit():
            # Asign a number to every name and get name for corresponing number
            name = dict(enumerate(self._vaults, start=1)).get(int(name), '')
        if name in self._vaults:
            self.game.start(name)
        else:
            utils.bprint('\nVault doesn\'t exist')

    def cb_ask_for_vault(self) -> None:
        """ When user choose to load already existing vault """
        # TODO sorting saves by recent play date
        self.game.stages.top().components.append(
            component.CommandOutput(
                *[f'List of all your vaults ({len(self._vaults)}):',
                '\n'.join([f'{i}. {f}' for i, f in enumerate(self._vaults, start=1)]),
                'Choose a vault to play on:']
            )
        )
        self.game.keyb.accumulate()

    def cb_new(self) -> None:
        utils.bprint('Pick a name for your vault: ', end='')
        name: str = ""
        if self.game.keyb.wait_for_enter():
            name = self.game.keyb.pop().strip()
        if name != '':
            self.game.start(name)
        else:
            utils.bprint('Vault\'s name not specified.')

    def cb_settings(self) -> None:
        # TODO settings stage
        print('settings will be here in the future')

    def cb_help(self) -> None:
        self.game.stages.top().show_credits()

    def cb_quit(self) -> None:
        self.game.quit()
