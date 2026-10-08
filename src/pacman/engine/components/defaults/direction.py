from enum import Enum

from ..component import Component


class Dir(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class Direction(Component):
    def __init__(
        self, direction: Dir, sprite_map: dict[Dir, list[str]]
    ) -> None:
        self.direction = direction
        self.sprite_map = sprite_map
