import utils
import command
import game
import ui.component as component


class Stage():

    commands: dict = dict()

    def __init__(self, name: str, g):
        self.game: game.Game = g
        self.name: str = name
        self.prompt: str = str()
        self.raw_prompt: str = str()
        self.prompt_items: list[str] = list()
        self.command_handler: command.CommandHandler = command.CommandHandlerFactory(self.game, self)
        self.components: list[component.UIComponent] = list()

    def loop(self) -> None:
        self.game.logger.error(f'Loop not inplemented for stage {self.name!r}')
        exit(1)

    def render(self, ts):
        self.game.logger.error(f'Rendering is not inplemented for stage {self.name!r}')
        exit(1)
    
    def show_credits(self):
        self.game.logger.error(f'Displaying credits is not implemented for stage {self.name!r}')
        exit(1)
    
    def close(self):
        self.game.logger.error(f'Closing is not implemented for stage {self.name!r}')
        exit(1)

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
            elif len(item) == 1:
                raw_items.append(item)
                final_items.append(item)
            elif item == '':
                raw_items.append(' ')
                final_items.append(' ')
            else:
                raw_items.append(str(self.game.vault.data[item]))
                final_items.append(str(self.game.vault.data[item]))
        self.prompt: str = ''.join(final_items)
        self.raw_prompt: str = ''.join(raw_items)


from stage.stages import MainMenu, GameStage, Inventory
