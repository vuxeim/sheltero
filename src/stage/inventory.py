import utils
import keyboard as kb
from stage import Stage
from utils import colorman


class InventoryStage(Stage):

    def __init__(self, game):
        super().__init__(game)
        self._previous_command: str = ""

    def loop(self) -> None:
        super().loop()
        self.update_prompt()
        if self.game.keyb.wait_for_enter():
            self.game.handle_command(self.game.keyb.pop())

    def handle(self, inp: str) -> None:
        cb = {kb.key.ENTER: self.cb_up,
              'close': lambda handler: handler.stage.close()
        }.get(inp)
        if cb is not None:
            cb()

    def close(self) -> None:
        utils.bprint('Inventory has been closed!')
        self.game.stages.pop()

    def cb_up(self) -> None:
        _len = len(self.game.keyb.input)
        self.game.keyb.input = self._previous_command
        if _len:
            back = colorman.CURSOR.BACK % _len
        else:
            back = ''
        utils.fprint(f'{back}{" "*_len}{back}{self.game.keyb.input}')
