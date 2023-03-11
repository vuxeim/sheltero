import os
import time
import logging


import config
import stage
import stage_stack
import vault
import utils
import keyboard
import text_component as component
import game.game_helper as game_helper
from utils import colorman


# TODO 1. organise return codes to work with either `exit(code_number)` or `return code_number`
# TODO 2. prevent the Traceback's output from growing by going from menu to game back and forth
# TODO 3. implement these things: (economy system) (denizens) (random events) (items) (craftings) (shops) (expeditions) (pets and other NPCs)
# TODO 5. use logging module in a bit more advanced way (https://docs.python.org/3/howto/logging-cookbook.html)
# TODO 4. implement language translations
# TODO 6. start writing tests


class Game():

    def __init__(self, path: str) -> None:
        self.play(path)

    def play(self, path: str) -> int:

        self.path: str = os.path.dirname(path)

        self.config: config.Config = config.load_config(self.path)

        _level_str: str = self.config.LOGGING.level.upper()
        _level_int: int = utils.log_levels.get(_level_str)
        logging.basicConfig(
            filename = self.config.LOGGING.file,
            level = _level_int,
            format = self.config.LOGGING.format
        )
        self.logger: logging.Logger = logging.getLogger()


        self.TPS: float = 1/game_helper.FPS
        # time elapsed from beginning of previous cycle to
        # beginning of current cycle (cycles are like frames)
        self.dt: float = 0.0
        self.timer: float = 0.0

        self.vault: vault.Vault | None = None

        _saves_path = os.path.join(self.path, 'saves')
        if not os.path.exists(_saves_path):
            os.mkdir(_saves_path)

        self.kb: keyboard.Keyboard = keyboard.Keyboard()

        self.stages: stage_stack.Stack = stage_stack.Stack()
        _main_menu_stage = stage.MainMenu(self)
        self.stages.push(_main_menu_stage)

        # Define list of text components to render
        _menu_layout = game_helper.get_menu_layout(self.path)
        _comp = component.GameMenu(_menu_layout)
        _components = []
        _components.append(_comp)
        self.components = _components

        self.running: bool = True
        return self.game_loop()

    def handle_command(self, cmd: str):
        """ Commands dispatcher. Calls command handler of current stage. """
        _stripped: str = cmd.strip()
        self.logger.debug(f'Invoked command {_stripped!r} in stage {self.stages.top().name!r}')
        self.stages.top().command_handler.execute(_stripped)

    def start(self, name: str) -> None:
        """ Effectively: loads vault, exits MainMenu stage and enters GameStage Stage"""
        self.vault: vault.Vault = vault.Vault(name, self.path)
        self.logger.debug(f'Started game in vault {name!r}')
        _text = f'\nWelcome in vault {self.vault.data["name"]!r}'
        p = colorman.Palette(colorman.FORE.RED)
        utils.bprint(p(_text))
        _game_stage = stage.GameStage(self)
        _appearance = self.config.PROMPT.appearance
        _game_stage.prompt_items: list[str] = _appearance.replace(' ','').split('.')[1:]
        _game_stage.update_prompt()
        self.stages.push(_game_stage)

    def quit(self) -> None:
        # NOTE in the future other acions should be stopped here
        self.kb.stop()
        self.running = False
        utils.clear_screen()

    def game_loop(self) -> int:
        self.prev_time = time.perf_counter()
        self.prev_size = os.get_terminal_size()
        utils.clear_screen()
        while self.running:

            time.sleep(self.TPS)
            self.now: float = time.perf_counter()
            self.dt: float = self.now - self.prev_time
            self.prev_time: float = self.now
            self.timer += self.dt

            self.size = os.get_terminal_size()
            if self.prev_size != self.size:
                utils.clear_screen()

            self.stages.top().render(self.size)
            self.stages.top().loop() # Blocking function

        return 0