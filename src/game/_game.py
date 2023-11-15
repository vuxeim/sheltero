"""
Contains class representing main game object
"""


from typing import TYPE_CHECKING
import os
import time

if TYPE_CHECKING:
    from keyboard_input import Keyboard
    from config import Config
import config
import stack
import stage
import vault
import utils
import keyboard_input
from ui import component
from game import helper
from utils import colorman


# TODO 3. implement these things: (economy system) (denizens) (random events) (items) (craftings) (shops) (expeditions) (pets and other NPCs)
# TODO 4. implement language translations
# TODO 6. start writing tests
# TODO 7. use pathlib to handle path-releated stuff


class Game:
    """ Main game object """

    def __init__(self, path: str) -> None:

        # Enter alternative screen buffer
        utils.fprint(colorman.BUFFER.ALTERNATIVE)

        self.path: str = os.path.dirname(path)

        self.config: Config = config.load_config(self.path)

        self.tps: float = 1/helper.FPS
        # time elapsed from beginning of previous cycle to
        # beginning of current cycle (cycles are like frames)
        self.delta: float = 0.0
        self.timer: float = 0.0

        self.vault: vault.Vault

        _saves_path = os.path.join(self.path, 'saves')
        if not os.path.exists(_saves_path):
            os.mkdir(_saves_path)

        self.keyb: Keyboard = keyboard_input.Keyboard()

        # Initialize stages stack
        self.stages: stack.Stack = stack.Stack()

        # Add MainMenu stage to game's stage stack
        _main_menu_stage = stage.MainMenuStage(self)
        self.stages.push(_main_menu_stage)

        # Add MainMenu UIComponent to MainMenu Stage's components
        _text_menu_layout = helper.get_menu_layout(self.path, self.config.GENERAL.lang)
        _main_menu_component = component.MainMenu()
        _choices = component.TextBox(_text_menu_layout)
        self.stages.top().components.append(_main_menu_component)
        self.stages.top().components.append(_choices)

        # Don't echo and hide blinking cursor
        self.keyb.echo = False
        self.keyb.cursor.hide()

        self.running: bool = True
        try: self.game_loop()
        except KeyboardInterrupt: self.quit()

    def handle_command(self, cmd: str) -> None:
        """ Command dispatcher. Calls command handler of current stage. """
        _stripped: str = cmd.strip()
        self.stages.top().command_handler.execute(_stripped)

    def start(self, name: str) -> None:
        """ Loads vault, push GameStage stage onto the stages stack"""

        self.vault = vault.Vault(name, self.path)

        _text = f"\nWelcome in vault '{self.vault.data.name}'"
        p = colorman.Palette(colorman.FORE.RED)
        utils.bprint(p(_text))

        _game_stage = stage.GameStage(self)
        _appearance = self.config.PROMPT.appearance
        _game_stage.prompt_items = _appearance.replace(' ', '').split('.')[1:]
        _game_stage.update_prompt()
        self.stages.push(_game_stage)

    def quit(self) -> None:
        """ Quits the entire game """
        self.keyb.stop()
        self.running = False
        utils.clear_screen()
        utils.fprint(colorman.BUFFER.NORMAL)

    def game_loop(self) -> None:
        """ The main game loop """
        self.prev_time = time.perf_counter()
        self.prev_size = os.get_terminal_size()
        while self.running:

            time.sleep(self.tps)
            self.now: float = time.perf_counter()
            self.delta: float = self.now - self.prev_time
            self.prev_time: float = self.now
            self.timer += self.delta

            self.size = os.get_terminal_size()

            utils.clear_screen()
            self.stages.top().render()
            self.stages.top().loop() # Blocking function
