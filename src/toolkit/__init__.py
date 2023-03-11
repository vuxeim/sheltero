import os
import pickle
import glob


from utils import colorman


def path():
    """Returns current path"""
    return os.path.dirname(__file__)[::-1].replace('toolkit'[::-1], '', 1)[:0:-1]

_path = path()

def saves():
    """Returns list of all saves"""
    return os.listdir(_path+'/saves')

def data(name):
    """Prints save's data"""
    if os.path.exists(f'{_path}/saves/{name}'):
        with open(f'{_path}/saves/{name}/{name}.dat', 'rb') as f:
            data = pickle.load(f)
        print('\n'.join([f"{colorman.FORE.BLUE}{str('{}')!r}: {colorman.FORE.YELLOW}{str('{}')} {colorman.FORE.RED}{str('{}')}{colorman.STYLE.RESET}".format(*data) for data in [[k, v, str(type(v))[8:-2]] for k, v in data.items()]]))
    else:
        print(f'Save {name!r} doesn\'t exist')

def todos():
    """Prints todos and notes"""

    def rep(line):
        # Remove some strings from line
        return [line := line.replace(r, '', 1) for r in ['#', 'TODO', 'NOTE', 'https://', 'http://']][-1].strip()

    def colorize():
        return '{}{}{}{}:{}{}{}{}'.format(
            " "*(NSPACE-len(str(file))),
            colorman.FORE.GREEN,
            file,
            colorman.FORE.BLUE,
            line_num,
            colorman.STYLE.RESET,
            " "*(LSPACE-len(str(line_num))),
            rep(line)
        )

    # Get all files from sheltero directory excludins ones from extras folder
    files = [file for file in glob.glob('**/*.py', recursive=True) if not file.startswith('extras/')]
    # Remove *this* file from files list
    files.remove('/'.join(__file__.split('/')[-2:]))

    # Max size for name
    NSPACE = 12
    # Max size for line number
    LSPACE = 4

    types = {'todo': (todos := []), 'note': (notes := [])}

    for file in files:
        with open(file, 'r') as f:
            line_num = 1
            while (line := f.readline()):
                if any(text in line for text in ['TODO', 'NOTE']):
                    xtype = 'todo' if ('TODO' or 'todo') in line else 'note' if 'NOTE' in line else ''
                    types[xtype].append(colorize())
                line_num += 1

    p_y = colorman.Palette(colorman.FORE.YELLOW)
    p_m = p_y + colorman.FORE.MAGENTA
    _todos = f'\nTODOs ({len(todos)}):'
    _notes = f'\nNOTEs ({len(notes)}):'
    print(p_y(_todos))
    print('\n'.join(todos))

    print(p_m(_notes))
    print('\n'.join(notes), '\n')
