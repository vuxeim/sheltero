import datetime
from typing import Callable

import getkey
import utils
from handler import CommandHandler
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
        self.command_handler = GameCommandHandler(game, self)

    def loop(self) -> None:
        super().loop()
        self.update_prompt()
        if self.game.keyb.wait_for_enter():
            self.game.handle_command(self.game.keyb.pop())


def up(handler: CommandHandler) -> None:
    _len = len(handler.game.keyb.input)
    handler.game.keyb.input = handler.previous_command
    back = (colorman.CURSOR.BACK % _len) if _len else ''
    utils.fprint(f'{back}{" "*_len}{back}{handler.game.keyb.input}')


def _help(handler: CommandHandler) -> None:
    handler.stage.components.append(
        component.CommandOutput(
            *['Use \'?\' for list of available actions',
            'and \'??\' for description of every command']
        )
    )


def single_question_mark(commands: dict[str, str]) -> Callable[[CommandHandler], None]:
    def fun(handler: CommandHandler) -> None:
        handler.stage.components.append(
            component.CommandOutput(
                *commands
            )
        )
    return fun

def double_question_mark(commands: dict[str, str]) -> Callable[[CommandHandler], None]:
    def fun(handler: CommandHandler) -> None:
        handler.stage.components.append(
            component.CommandOutput(
                *['Available commands:',
                '\n'.join([f'{k} - {v}' for k, v in commands.items()])]
            )
        )
    return fun


def inventory(handler: CommandHandler) -> None:
    handler.game.stages.push(InventoryStage(handler.game))


def _exit(handler: CommandHandler) -> None:
    p = colorman.Palette(colorman.FORE.YELLOW)
    handler.game.vault.save()
    play_time = utils.nice_time(datetime.datetime.now() - handler.game.vault.data.beg_time)
    _text = p(f'See you later!\nYou have been playing for: {play_time}')
    handler.stage.components = [component.CommandOutput(_text),]
    handler.game.stages.pop()


def info(handler: CommandHandler) -> None:
    p_gray = colorman.Palette(colorman.FORE.BRIGHT.WHITE)
    p_yellow = colorman.Palette(colorman.FORE.YELLOW)
    p_red = colorman.Palette(colorman.FORE.RED)
    _hash = p_gray(' # ')
    _escaped = p_yellow('Vault\'s name: ')
    _name = p_red(utils.nice_time(handler.game.vault.data.name))
    _creation = p_red(utils.nice_time(handler.game.vault.data.creation_date))
    _denizens = p_red(str(handler.game.vault.data.denizens))
    _time = p_red(utils.nice_time(handler.game.vault.data.play_time + datetime.datetime.now() - handler.game.vault.data.beg_time))
    _session = p_red(utils.nice_time(datetime.datetime.now() - handler.game.vault.data.beg_time))
    handler.stage.components.append(
        component.CommandOutput(
            *[f"{_hash}{_escaped}{_name}",
            f"{_hash}{p_yellow('Vault was created: ')}{_creation}",
            f"{_hash}{p_yellow('Numbers of denizens: ')}{_denizens}",
            f"{_hash}{p_yellow('Total playing time: ')}{_time}",
            f"{_hash}{p_yellow('You have been playing for: ')}{_session}"]
        )
    )


class GameCommandHandler(CommandHandler):

    commands: dict[str, str] = {
        'help': 'print info about ? and ??',
        '?': 'list of available actions',
        '??': 'description of every command',
        'inv': 'open the inventory',
        'info': 'see vault\'s info',
        'exit': 'save a game and exit to menu'
    }

    @staticmethod
    def nop(handler: CommandHandler) -> None:
        handler.stage.components.append(
            component.CommandOutput('I dunno how to respond to that... Use \'help\' to get help')
            )

    callbacks = {
        getkey.key.UP: up,
        'help': _help,
        '?': single_question_mark(commands),
        '??': double_question_mark(commands),
        'inv': inventory,
        'info': info,
        'exit': _exit,
    }
