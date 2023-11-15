from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game
    from handler import CommandHandler
import utils
from ui import component


class Stage:
    # TODO abstract class???

    def __init__(self, game):
        self.game: Game = game
        self.prompt: str = str()
        self.raw_prompt: str = str()
        self.prompt_items: list[str] = []
        self.components: list[component.UIComponent] = []
        self.command_handler: CommandHandler

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def loop(self) -> None:
        self.components = [c for c in self.components if c]

    def show_credits(self):
        raise NotImplementedError(f'Displaying credits is not implemented for stage {self.name}')

    def close(self):
        raise NotImplementedError(f'Closing is not implemented for stage {self.name}')

    def render(self):
        for component in self.components:
            component.render(self.game)

    def update_prompt(self) -> None:
        final_items: list = []
        raw_items: list = []
        for item in self.prompt_items:
            if item in utils.colors.keys():
                _code = '\x1b[' + str(utils.colors[item]) + 'm'
                final_items.append(_code)
            elif item == 'stage':
                raw_items.append(self.name)
                final_items.append(self.name)
            elif item == 'name':
                raw_items.append(self.game.vault.data.name)
                final_items.append(self.game.vault.data.name)
            elif item == 'balance':
                raw_items.append(str(self.game.vault.data.balance))
                final_items.append(str(self.game.vault.data.balance))
            elif item == 'denizens':
                raw_items.append(str(self.game.vault.data.denizens))
                final_items.append(str(self.game.vault.data.denizens))
            elif len(item) == 1:
                raw_items.append(item)
                final_items.append(item)
            elif item == '':
                raw_items.append(' ')
                final_items.append(' ')
            else:
                # Use smth else than exception here
                raise NameError(f"Unknown prompt element in config '{item}'")
        self.prompt: str = ''.join(final_items)
        self.raw_prompt: str = ''.join(raw_items)


# export classes
from stage.develop import DevelopStage
from stage.inventory import InventoryStage
from stage.game import GameStage
from stage.mainmenu import MainMenuStage
