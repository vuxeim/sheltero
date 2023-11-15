import os
import tomllib
from typing import Any


class Config:

    class GENERAL:
        lang: str

    class PROMPT:
        appearance: str


def load_config(path: str) -> Config:

    _user_config = os.path.join(path, 'config.toml')
    _default_config = os.path.join(path, 'resources', 'texts', 'config.toml')
    if not os.path.exists(_user_config):
        if os.path.exists(_default_config):
            with open(_default_config) as f:
                _conf: str = f.read()
            with open(_user_config, 'w') as g:
                g.write(_conf)
        else:
            exit(f'`{_default_config}` file doesn\'t exist')
    with open(_user_config, 'rb') as h:
        cfg: dict[str, Any] = tomllib.load(h)

    class _Config(Config):
        class GENERAL:
            lang: str = cfg['GENERAL']['lang']

        class PROMPT:
            appearance: str = cfg['PROMPT']['appearance']

    return _Config()
