from collections.abc import Callable

import pyray as pr

from pacman.engine.components.component import Component


class KeyHook(Component):
    def __init__(self, keys: dict[pr.KeyboardKey, Callable]) -> None:
        self.keys = keys
