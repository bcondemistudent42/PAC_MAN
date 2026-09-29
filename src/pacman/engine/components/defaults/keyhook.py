import pyray as pr

from pacman.engine.components.component import Component
from pacman.engine.components.defaults.direction import Dir


class KeyHook(Component):
    def __init__(self, keys: dict[pr.KeyboardKey, Dir]) -> None:
        self.keys = keys
