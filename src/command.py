from types import SimpleNamespace
import os
import datetime
import colorama


import stage
import utils
import game
import getkey
import text_component as component


class CommandHandler:

    previous_command: str = str()

    def __init__(self, g) -> None:
        self.game: game.Game = g

    def execute(self, cmd: str): ...


class CommandHandlerFactory:

    def __new__(cls, g, stg) -> CommandHandler:
        
        # TODO How to do it nicer?

        if isinstance(stg, stage.MainMenu):
            return MainMenuCommandHandler(g)

        if isinstance(stg, stage.GameStage):
            return GameCommandHandler(g)
        
        if isinstance(stg, stage.Inventory):
            return InventoryCommandHandler(g)
        
        g.logger.error(f'CommandHandler is not implemented for stage {stg.name!r}')
        exit(1)


class MainMenuCommandHandler(CommandHandler):

    def execute(self, cmd: str):

        self.previous_command = cmd

        if cmd == 'l':
            # TODO sorting saves by last play date
            _path: str = os.path.join(self.game.path, 'saves')
            vaults: set[str] = set(d for d in os.listdir(_path) if os.path.isdir(os.path.join(_path, d)))
            self.game.components.append(
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
            if not name:
                utils.bprint('Vault\'s name not specified.')
            else:
                self.game.start(name)

        elif cmd == 's':
            print('settings will be here in the future')

        elif cmd == 'h':
            self.game.stages.top().show_credits()

        elif cmd == 'q':
            self.game.quit()


class GameCommandHandler(CommandHandler):

    def execute(self, cmd: str):

        if cmd == getkey.key.UP:
            _len = len(self.game.kb.input)
            self.game.kb.input = self.previous_command
            back = colorama.Cursor.BACK(_len) if _len else ''
            utils.fprint(f'{back}{" "*_len}{back}{self.game.kb.input}')

        elif cmd == 'help':
            self.game.components.append(
                component.CommandOutput(
                    *['Use \'?\' for list of available actions',
                    'and \'??\' for description of every command']
                )
            )

        elif cmd == '?':
            self.game.components.append(
                component.CommandOutput(
                    *self.game.stages.top().commands
                )
            )

        elif cmd == '??':
            self.game.components.append(
                component.CommandOutput(
                    *['Available commands:',
                    '\n'.join([f'{k} - {v}' for k, v in self.game.stages.top().commands.items()])]
                )
            )

        elif cmd == 'inv':
            self.game.stages.push(stage.Inventory(self.game))

        elif cmd == 'info':
            C = SimpleNamespace(yellow='\x1b[33m', red='\x1b[31m', reset='\x1b[0m', grey='\x1b[30m')
            self.game.components.append(
                component.CommandOutput(
                    *[f" {C.grey}# {C.yellow}Vault\'s name: {C.red}{utils.nice_time(self.game.vault.data['name'])}{C.reset}",
                    f" {C.grey}# {C.yellow}Vault was created: {C.red}{utils.nice_time(self.game.vault.data['creation_date'])}{C.reset}",
                    f" {C.grey}# {C.yellow}Numbers of denizens: {C.red}{self.game.vault.data['denizens']}{C.reset}",
                    f" {C.grey}# {C.yellow}Total playing time: {C.red}{utils.nice_time(self.game.vault.data['play_time'] + datetime.datetime.now() - self.game.vault.data['beg_time'])}{C.reset}",
                    f" {C.grey}# {C.yellow}You have been playing for: {C.red}{utils.nice_time(datetime.datetime.now() - self.game.vault.data['beg_time'])}{C.reset}"]
                )
            )
    
        elif cmd == 'exit':
            self.game.vault.save()
            play_time = utils.nice_time(datetime.datetime.now() - self.game.vault.data['beg_time'])
            self.game.components = [component.CommandOutput(f'{colorama.Fore.YELLOW}See you later!\nYou have been playing for: {play_time}{colorama.Fore.RESET}'),]
            self.game.stages.pop()

        else:
            self.game.components.append(component.CommandOutput('I dunno how to respond to that... Use \'help\' to get help'))


class InventoryCommandHandler(CommandHandler):

    def execute(self, cmd: str):

        if cmd == getkey.key.UP:
            _len = len(self.game.kb.input)
            self.game.kb.input = self.previous_command
            if _len:
                back = colorama.Cursor.BACK(_len)
            else:
                back = ''
            utils.fprint('{}{" "*_len}{}{}'.format(
                    back, back, self.game.kb.input
            ))

        if cmd == 'close':
            self.game.stages.top().close()
