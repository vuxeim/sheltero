from __future__ import annotations
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from game import Game
    from stage import Stage


class CommandHandler:

    previous_command: str = str()
    callbacks: dict[str, Callable[[CommandHandler], None]]

    def __init__(self, game: Game, stage: Stage) -> None:
        self.game: Game = game
        self.stage: Stage = stage

    @staticmethod
    def nop(handler: CommandHandler) -> None: ...

    def execute(self, cmd: str) -> None:
        self.previous_command = cmd
        self.callbacks.setdefault(cmd, self.nop)(self)