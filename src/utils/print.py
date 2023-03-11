import sys
import time


def bprint(*text: str, sleep: float = 0.003, sep: str = ' ', end: str = '\n') -> None:
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


def nice_time(time) -> str:
    return str(time).split(".")[0]


def clear_screen() -> None:
    sys.stdout.write("\x1b[2J")
    sys.stdout.flush()