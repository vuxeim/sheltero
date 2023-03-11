import os


from stage import Stage
import utils


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
