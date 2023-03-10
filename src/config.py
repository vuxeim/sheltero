import os
import tomllib
from typing import Any

class Config:

    class LOGGING:

        level: str
        file: str
        format: str
    
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

    class Config:

        class LOGGING:

            level: str = cfg['LOGGING']['level']
            file: str = cfg['LOGGING']['file']
            format: str = cfg['LOGGING']['format']
        
        class PROMPT:
            
            appearance: str = cfg['PROMPT']['appearance']

    return Config