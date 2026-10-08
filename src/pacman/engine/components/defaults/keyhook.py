import pyray as pr

from ..component import Component
from .direction import Dir


class KeyHook(Component):
    def __init__(self, keys: dict[pr.KeyboardKey, Dir]) -> None:
        self.keys = keys
