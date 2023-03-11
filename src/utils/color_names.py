from utils import colorman


colors: dict[str, int] = {
    'BLACK': colorman.FORE.BLACK,
    'RED': colorman.FORE.RED,
    'GREEN': colorman.FORE.GREEN,
    'YELLOW': colorman.FORE.YELLOW,
    'BLUE': colorman.FORE.BLUE,
    'MAGENTA': colorman.FORE.MAGENTA,
    'CYAN': colorman.FORE.CYAN,
    'WHITE': colorman.FORE.WHITE,

    'LIGHTBLACK': colorman.FORE.BRIGHT.BLACK,
    'LIGHTRED': colorman.FORE.BRIGHT.RED,
    'LIGHTGREEN': colorman.FORE.BRIGHT.GREEN,
    'LIGHTYELLOW': colorman.FORE.BRIGHT.YELLOW,
    'LIGHTBLUE': colorman.FORE.BRIGHT.BLUE,
    'LIGHTMAGENTA': colorman.FORE.BRIGHT.MAGENTA,
    'LIGHTCYAN': colorman.FORE.BRIGHT.CYAN,
    'LIGHTWHITE': colorman.FORE.BRIGHT.WHITE,

    'RESET': colorman.STYLE.RESET,
}
