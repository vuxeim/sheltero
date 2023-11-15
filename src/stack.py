"""
Abstraction layer representing stack of stages
"""


from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stage import Stage


class Stack:

    def __init__(self) -> None:
        self._stack = list()

    def top(self) -> Stage:
        return self._stack[-1]

    def push(self, stg: Stage) -> None:
        self._stack.append(stg)

    def pop(self) -> Stage:
        return self._stack.pop()
