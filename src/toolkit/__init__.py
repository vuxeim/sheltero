import os
import pickle
import colorama
import glob

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
        print('\n'.join([f"{colorama.Fore.BLUE}{str('{}')!r}: {colorama.Fore.YELLOW}{str('{}')} {colorama.Fore.RED}{str('{}')}{colorama.Fore.RESET}".format(*data) for data in [[k, v, str(type(v))[8:-2]] for k, v in data.items()]]))
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
            colorama.Fore.GREEN,
            file,
            colorama.Fore.BLUE,
            line_num,
            colorama.Fore.RESET,
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

    print(f'\n{colorama.Fore.YELLOW}TODOs ({len(todos)}): {colorama.Fore.RESET}')
    print('\n'.join(todos))

    print(f'\n{colorama.Fore.MAGENTA}NOTEs ({len(notes)}): {colorama.Fore.RESET}')
    print('\n'.join(notes), '\n')
