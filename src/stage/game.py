import datetime

import utils
import keyboard
from stage import Stage, InventoryStage
from ui import component
from utils import colorman


class GameStage(Stage):
    """
    The main stage.
    Used after choosing vault to play.
    """

    def __init__(self, game):
        super().__init__(game)
        self._previous_command: str = ""
        self._commands: dict[str, str] = {
            'help': 'print info about ? and ??',
            '?': 'list of available actions',
            '??': 'description of every command',
            'inv': 'open the inventory',
            'info': 'see vault\'s info',
            'exit': 'save a game and exit to menu'
        }
        self._cmd: str = ""
        self._history: list[str] = []
        self.game.keyb.accumulate()

    def loop(self) -> None:
        super().loop()
        self.update_prompt()

        self._cmd = self.game.keyb.collect()
        if self._cmd is not None:
            self.handle(self._cmd)

    def handle(self, inp: str) -> None:
        cb = {keyboard.key.UP: self.cb_up,
              'help': self.cb_help,
              '?': self.cb_single_question_mark,
              '??': self.cb_double_question_mark,
              'inv': self.cb_inventory,
              'info': self.cb_info,
              'exit': self.cb_exit,
            }.get(inp)
        if cb is not None:
            cb()

    def close(self) -> None:
        pass

    def cb_nop(self) -> None:
        self.game.stages.top().components.append(
            component.CommandOutput('I dunno how to respond to that... Use \'help\' to get help')
            )

    def cb_up(self) -> None:
        _len = len(self._cmd)
        back = (colorman.CURSOR.BACK % _len) if _len else ''
        utils.fprint(f'{back}{" "*_len}{back}{self._previous_command}')

    def cb_help(self) -> None:
        self.game.stages.top().components.append(
            component.CommandOutput(
                *['Use \'?\' for list of available actions',
                'and \'??\' for description of every command']
            )
        )

    def cb_single_question_mark(self) -> None:
        self.game.stages.top().components.append(
            component.CommandOutput(
                *self._commands
            )
        )

    def cb_double_question_mark(self) -> None:
        self.game.stages.top().components.append(
            component.CommandOutput(
                *['Available commands:',
                '\n'.join([f'{k} - {v}' for k, v in self._commands.items()])]
            )
        )

    def cb_inventory(self) -> None:
        self.game.stages.push(InventoryStage(self.game))

    def cb_exit(self) -> None:
        p = colorman.Palette(colorman.FORE.YELLOW)
        self.game.vault.save()
        play_time = utils.nice_time(datetime.datetime.now() - self.game.vault.data.beg_time)
        _text = p(f'See you later!\nYou have been playing for: {play_time}')
        self.game.stages.top().components = [component.CommandOutput(_text),]
        self.game.stages.pop()

    def cb_info(self) -> None:
        p_gray = colorman.Palette(colorman.FORE.BRIGHT.WHITE)
        p_yellow = colorman.Palette(colorman.FORE.YELLOW)
        p_red = colorman.Palette(colorman.FORE.RED)
        _hash = p_gray(' # ')
        _escaped = p_yellow('Vault\'s name: ')
        _name = p_red(utils.nice_time(self.game.vault.data.name))
        _creation = p_red(utils.nice_time(self.game.vault.data.creation_date))
        _denizens = p_red(str(self.game.vault.data.denizens))
        _time = p_red(utils.nice_time(self.game.vault.data.play_time + datetime.datetime.now() - self.game.vault.data.beg_time))
        _session = p_red(utils.nice_time(datetime.datetime.now() - self.game.vault.data.beg_time))
        self.game.stages.top().components.append(
            component.CommandOutput(
                *[f"{_hash}{_escaped}{_name}",
                f"{_hash}{p_yellow('Vault was created: ')}{_creation}",
                f"{_hash}{p_yellow('Numbers of denizens: ')}{_denizens}",
                f"{_hash}{p_yellow('Total playing time: ')}{_time}",
                f"{_hash}{p_yellow('You have been playing for: ')}{_session}"]
            )
        )
