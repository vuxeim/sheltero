from stage import Stage
import utils


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
