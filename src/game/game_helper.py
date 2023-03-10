import os


FPS = 20


def get_menu_layout(path: str) -> list[str]:
    _full_path: str = os.path.join(path, 'resources', 'texts', 'menu.txt')
    with open(_full_path) as f:
        layout: list[str] = f.readlines()
    return layout