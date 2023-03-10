import sys
import time
import colorama

# TODO rewrite colorama

def nice_time(time) -> str:
    return str(time).split(".")[0]

# NOTE Change sleep to 0.03 in production
def bprint(*text: str, sleep: float = 0.0, sep: str = ' ', end: str = '\n') -> None:
    for char in sep.join(text):
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(sleep)
    sys.stdout.write(end)
    sys.stdout.flush()

def fprint(text: str) -> None:
    bprint(text, sleep=0, sep='', end='')

def pprint(x: int, y: int, text: str) -> None:
    sys.stdout.write(f"\x1b7\x1b[{x};{y}f{text}\x1b8")
    sys.stdout.flush()

def clear_screen() -> None:
    sys.stdout.write("\x1b[2J")
    sys.stdout.flush()

def cmove(x: int, y: int) -> None:
    # NOTE not sure if incrementing y is good solution
    sys.stdout.write(f"\033[{x};{y+1}H")
    sys.stdout.flush()

log_levels: dict[str, int] = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0,
}

colors: dict[str, str] = {
    'BLACK': colorama.Fore.BLACK,
    'BLUE': colorama.Fore.BLUE,
    'CYAN': colorama.Fore.CYAN,
    'GREEN': colorama.Fore.GREEN,
    'MAGENTA': colorama.Fore.MAGENTA,
    'RED': colorama.Fore.RED,
    'WHITE': colorama.Fore.WHITE,
    'YELLOW': colorama.Fore.YELLOW,

    'LIGHTBLACK': colorama.Fore.LIGHTBLACK_EX,
    'LIGHTBLUE': colorama.Fore.LIGHTBLUE_EX,
    'LIGHTCYAN': colorama.Fore.LIGHTCYAN_EX,
    'LIGHTGREEN': colorama.Fore.LIGHTGREEN_EX,
    'LIGHTMAGENTA': colorama.Fore.LIGHTMAGENTA_EX,
    'LIGHTRED': colorama.Fore.LIGHTRED_EX,
    'LIGHTWHITE': colorama.Fore.LIGHTWHITE_EX,
    'LIGHTYELLOW': colorama.Fore.LIGHTYELLOW_EX,

    'RESET': colorama.Fore.RESET,
}
