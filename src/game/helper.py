"""
Contains helper functions for game module
"""


import os


FPS = 20


def get_menu_layout(path: str, lang: str) -> list[str]:
    """ Resturns textual menu in selected language """
    _full_path: str = os.path.join(path, 'resources', 'texts', lang, 'menu.txt')
    with open(_full_path) as file:
        layout: list[str] = file.readlines()
    return [line.strip() for line in layout]
