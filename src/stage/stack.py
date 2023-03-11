import stage

class Stack:

    def __init__(self) -> None:
        self._stack = list()

    def top(self) -> stage.Stage:
        return self._stack[-1]
    
    def push(self, stage: stage.Stage) -> None:
        self._stack.append(stage)
    
    def pop(self) -> stage.Stage:
        return self._stack.pop()