import os
import datetime


import stage
import utils
import game
import getkey
import ui.component as component
from utils import colorman


class CommandHandler:

    previous_command: str = str()

    def __init__(self, g, stg) -> None:
        self.game: game.Game = g
        self.stage: stage.Stage = stg

    def execute(self, cmd: str): ...


class CommandHandlerFactory:

    def __new__(cls, g, stg) -> CommandHandler:
        
        # TODO How to do it in a nicer way?

        if isinstance(stg, stage.MainMenu):
            return MainMenuCommandHandler(g, stg)

        if isinstance(stg, stage.GameStage):
            return GameCommandHandler(g, stg)
        
        if isinstance(stg, stage.Inventory):
            return InventoryCommandHandler(g, stg)
        
        g.logger.error(f'CommandHandler is not implemented for stage {stg.name!r}')
        exit(1)


class MainMenuCommandHandler(CommandHandler):

    def execute(self, cmd: str):

        self.previous_command = cmd

        if cmd == 'l':
            # TODO sorting saves by last play date
            _path: str = os.path.join(self.game.path, 'saves')
            vaults: set[str] = set(d for d in os.listdir(_path) if os.path.isdir(os.path.join(_path, d)))
            self.stage.components.append(
                component.CommandOutput(
                    *[f'List of all your vaults ({len(vaults)}):',
                    '\n'.join([f'{i}. {f}' for i, f in enumerate(vaults, start=1)]),
                    f'Choose a vault to play on:']
                )
            )
            name: str = ""
            if self.game.kb.wait_for_enter():
                name = self.game.kb.pop().strip()
            if name.isdigit():
                # Asign a number to every name and get name of corresponing number
                name: str = {i: name for i, name in enumerate(vaults, start=1)}.get(int(name), '')
            if name in vaults:
                self.game.start(name)
            else:
                print('\nVault doesn\'t exist')

        elif cmd == 'n':
            utils.bprint('Pick a name for your vault: ', end='')
            name: str = ""
            if self.game.kb.wait_for_enter():
                name = self.game.kb.pop().strip()
            if name != '':
                self.game.start(name)
            else:
                utils.bprint('Vault\'s name not specified.')

        elif cmd == 's':
            print('settings will be here in the future')

        elif cmd == 'h':
            self.stage.show_credits()

        elif cmd == 'q':
            self.game.quit()


class GameCommandHandler(CommandHandler):

    def execute(self, cmd: str):

        if cmd == getkey.key.UP:
            _len = len(self.game.kb.input)
            self.game.kb.input = self.previous_command
            back = colorman.CURSOR.BACK(_len) if _len else ''
            utils.fprint(f'{back}{" "*_len}{back}{self.game.kb.input}')

        elif cmd == 'help':
            self.stage.components.append(
                component.CommandOutput(
                    *['Use \'?\' for list of available actions',
                    'and \'??\' for description of every command']
                )
            )

        elif cmd == '?':
            self.stage.components.append(
                component.CommandOutput(
                    *self.stage.commands
                )
            )

        elif cmd == '??':
            self.stage.components.append(
                component.CommandOutput(
                    *['Available commands:',
                    '\n'.join([f'{k} - {v}' for k, v in self.stage.commands.items()])]
                )
            )

        elif cmd == 'inv':
            self.game.stages.push(stage.Inventory(self.game))

        elif cmd == 'info':
            p_gray = colorman.Palette(colorman.FORE.BRIGHT.WHITE)
            p_yellow = p_gray + colorman.FORE.YELLOW
            p_red = p_gray + colorman.FORE.RED
            _hash = p_gray(' # ')
            _escaped = p_yellow('Vault\'s name: ')
            _name = p_red(utils.nice_time(self.game.vault.data['name']))
            _creation = p_red(utils.nice_time(self.game.vault.data['creation_date']))
            _denizens = p_red(str(self.game.vault.data['denizens']))
            _time = p_red(utils.nice_time(self.game.vault.data['play_time'] + datetime.datetime.now() - self.game.vault.data['beg_time']))
            _session = p_red(utils.nice_time(datetime.datetime.now() - self.game.vault.data['beg_time']))
            self.stage.components.append(
                component.CommandOutput(
                    *[f"{_hash}{_escaped}{_name}",
                    f"{_hash}{p_yellow('Vault was created: ')}{_creation}",
                    f"{_hash}{p_yellow('Numbers of denizens: ')}{_denizens}",
                    f"{_hash}{p_yellow('Total playing time: ')}{_time}",
                    f"{_hash}{p_yellow('You have been playing for: ')}{_session}"]
                )
            )
    
        elif cmd == 'exit':
            p = colorman.Palette(colorman.FORE.YELLOW)

            self.game.vault.save()
            play_time = utils.nice_time(datetime.datetime.now() - self.game.vault.data['beg_time'])
            _text = p(f'See you later!\nYou have been playing for: {play_time}')
            self.stage.components = [component.CommandOutput(_text),]
            self.game.stages.pop()

        else:
            self.stage.components.append(component.CommandOutput('I dunno how to respond to that... Use \'help\' to get help'))


class InventoryCommandHandler(CommandHandler):

    def execute(self, cmd: str):

        if cmd == getkey.key.UP:
            _len = len(self.game.kb.input)
            self.game.kb.input = self.previous_command
            if _len:
                back = colorman.CURSOR.BACK(_len)
            else:
                back = ''
            utils.fprint('{}{" "*_len}{}{}'.format(
                    back, back, self.game.kb.input
            ))

        if cmd == 'close':
            self.stage.close()
