from pacman.engine.components.component import Component
from collections.abc import Callable
import pyray as pr

class KeyHook(Component):
    def __init__(self, keys: dict[pr.KeyboardKey, Callable]) -> None:
        self.keys = keys
