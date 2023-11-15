import os
import time
import threading

import utils
import getkey
from utils import colorman

class _NtCursor:

    import ctypes
    class _CursorInfo(ctypes.Structure):
        import ctypes
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

    @staticmethod
    def hide():
        raise NotImplementedError()

    @staticmethod
    def show():
        raise NotImplementedError()

class _PosixCursor:

    @staticmethod
    def hide():
        utils.fprint('\x1b[?25l')

    @staticmethod
    def show():
        utils.fprint('\x1b[?25h')

class _Cursor:

    if os.name == 'nt':
        impl = _NtCursor()
    elif os.name == 'posix':
        impl = _PosixCursor()
    else:
        # TODO better way to determine platform
        raise Exception('Unsupported platform')

    hide = impl.hide
    show = impl.show

# https://stackoverflow.com/a/57387909
class KeyboardThread(threading.Thread):

    def __init__(self, input_callback):
        self.input_callback = input_callback
        self.running: bool = True
        super(KeyboardThread, self).__init__(name='keyboard-thread')
        self.daemon: bool = True
        self.start()

    def run(self) -> None:
        while self.running:
            self.input_callback(getkey.getkey())

class Keyboard:

    def __init__(self):
        self.echo: bool = True
        self.input: str = str()
        self.thread = KeyboardThread(self.receive)
        self.cursor: type[_Cursor] = _Cursor

    def receive(self, inp) -> None:
        if inp == getkey.key.BACKSPACE:
            if len(self.input):
                self.input = self.input[:-1]
                utils.fprint(
                    colorman.CURSOR.BACK % 1 +
                    ' ' + colorman.CURSOR.BACK % 1
                    )
        elif inp == getkey.key.ENTER:
            self.input += inp
        else:
            self.input += inp
            if self.echo:
                utils.fprint(self.input[-1])

    def pop(self) -> str:
        input, self.input = self.input, ''
        return input

    # TODO find non-blocking way to handle input
    def wait_for_enter(self) -> bool:
        while True:
            if str(self.input).endswith(getkey.key.ENTER):
                return True
            time.sleep(1/40)

    def wait_for_input(self) -> bool:
        while True:
            if self.input:
                return True
            time.sleep(1/40)

    def stop(self) -> None:
        """ Safely kills the keyboard thread """
        self.thread.running = False
        self.cursor.show()