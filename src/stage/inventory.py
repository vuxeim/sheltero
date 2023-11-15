import getkey
import utils
from handler import CommandHandler
from stage import Stage
from utils import colorman


class InventoryStage(Stage):

    def __init__(self, game):
        super().__init__(game)
        self.command_handler = InventoryCommandHandler(game, self)

    def loop(self) -> None:
        super().loop()
        self.update_prompt()
        if self.game.keyb.wait_for_enter():
            self.game.handle_command(self.game.keyb.pop())

    def close(self) -> None:
        utils.bprint('Inventory has been closed!')
        self.game.stages.pop()

def up(handler: CommandHandler) -> None:
    _len = len(handler.game.keyb.input)
    handler.game.keyb.input = handler.previous_command
    if _len:
        back = colorman.CURSOR.BACK % _len
    else:
        back = ''
    utils.fprint('{}{" "*_len}{}{}'.format(
            back, back, handler.game.keyb.input
    ))

class InventoryCommandHandler(CommandHandler):

    callbacks = {
        getkey.key.UP: up,
        'close': lambda handler: handler.stage.close()
    }
