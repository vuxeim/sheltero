import glob
import os
import pickle

import utils
from handler import CommandHandler
from stage import Stage
from utils import colorman


class DevelopStage(Stage):
    """
    The main stage.
    Used after choosing vault to play.
    """

    def __init__(self, game):
        super().__init__(game)
        self.command_handler = DevelopCommandHandler(game, self)

    def loop(self) -> None:
        super().loop()
        self.update_prompt()
        if self.game.keyb.wait_for_enter():
            self.game.handle_command(self.game.keyb.pop())


def path():
    """Returns sheltero path"""
    return os.path.dirname(os.path.dirname(__file__))


def print_title() -> None:
    segments = utils.square_read(os.path.join(path(), 'resources', 'rexts', 'sheltero_title'))
    for s in segments:
        print(s)


def saves(_path: str):
    """Returns list of all saves"""
    _saves_dir = os.path.join(_path, 'saves')
    return os.listdir(_saves_dir)


def data(name: str):
    """Prints save's data"""
    # TODO go back there

    _full_path = os.path.join(path(), 'saves', name)
    if not os.path.exists(_full_path):
        print(f'Save {name!r} doesn\'t exist')
        return

    _file = os.path.join(_full_path, name+'.dat')
    with open(_file, 'rb') as f:
        data = pickle.load(f)

    p_b = colorman.Palette(colorman.FORE.BLUE)
    p_y = p_b + colorman.FORE.YELLOW
    p_r = p_b + colorman.FORE.RED

    for k, v in data.items():

        _key = p_b(str(k))
        _val = p_y(str(v))
        _type = p_r(str(type(v))[8:-2])

        _line = f'\'{_key}\': {_val} {_type}'
        print(_line)


def todos():
    """Prints todos and notes"""

    p_y = colorman.Palette(colorman.FORE.YELLOW)
    p_m = p_y + colorman.FORE.MAGENTA
    p_g = p_y + colorman.FORE.GREEN
    p_b = p_y + colorman.FORE.BLUE

    def colorize(file: str, line_num: int, line: str):

        def rep(line):
            # Remove some strings from line
            _unwanted = '# TODO NOTE https:// http://'.split()
            _steps = [line := line.replace(r, '', 1) for r in _unwanted]
            _last = _steps[-1]
            return _last.strip()

        NSPACE = 12 # Max size for name
        LSPACE = 4 # Max size for line number

        _name_space = " " * (NSPACE - len(file))
        _line_space = " " * (LSPACE - len(str(line_num)))

        _replaced = rep(line)
        _colored_file = p_g(file)
        _colored_line_num = p_b(str(line_num))

        return '{}{}:{}{}{}'.format(
            _name_space,
            _colored_file,
            _colored_line_num,
            _line_space,
            _replaced
        )

    # Get all files from sheltero directory
    files = [file for file in glob.glob('**/*.py', recursive=True)]
    # Remove *this* file from files list
    files.remove('/'.join(__file__.split('/')[-2:]))

    todos = []
    notes = []
    types = {'todo': todos, 'note': notes}

    for file in files:
        with open(file, 'r') as f:

            line_num = 1
            while (line := f.readline()):

                _all_lower = line.lower()
                for name, is_present in [(text, text in _all_lower) for text in ['todo', 'note']]:

                    if is_present:
                        _colorized_line = colorize(file, line_num, line)
                        types[name].append(_colorized_line)

                line_num += 1

    _todos_header = f'\nTODOs ({len(todos)}):'
    print(p_y(_todos_header))
    print('\n'.join(todos))

    _notes_header = f'\nNOTEs ({len(notes)}):'
    print(p_m(_notes_header))
    print('\n'.join(notes), '\n')


class DevelopCommandHandler(CommandHandler):

        """
        tools = []
        for name, item in inspect.getmembers(_tk):
            if not name.startswith('_') and name not in [module[0] for module in inspect.getmembers(_tk, inspect.ismodule)]:
                if name not in dir(__builtins__) and name not in locals().keys() and name not in globals().keys():
                    pair = {name: item}
                    locals().update(pair)
                    globals().update(pair)
                    tools.append([str(type(item))[8:-2], name, item])
                else:
                    print(f'ERROR!!! {name!r} already exists in scope')

        # ignore error with path() not defined
        print('Welcome in sheltero tools!', path())
        for tool_type in set([tool[0] for tool in tools]):
            print(tool_type+'s:')
            for item in sorted(tools, key=lambda item: item[0]):
                if item[0] == tool_type:
                    print(f'\t{item[1]} - {item[2].__doc__ or ""}')
        """