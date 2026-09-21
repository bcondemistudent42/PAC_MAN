from enum import Enum

from pacman.engine.components.component import Component


class Dir(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class Direction(Component):
    def __init__(self, direction: Dir) -> None:
        self.direction = direction
