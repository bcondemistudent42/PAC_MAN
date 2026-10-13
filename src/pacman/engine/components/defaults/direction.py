from enum import Enum

from ..component import Component


class Dir(Enum):
    """Available movement directions."""

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class Direction(Component):
    """Store an entity's current direction and directional sprites."""

    def __init__(
        self, direction: Dir, sprite_map: dict[Dir, list[str]]
    ) -> None:
        """Create a direction component.

        Args:
            direction: Initial movement direction.
            sprite_map: Sprite names grouped by direction.
        """
        self.direction = direction
        self.sprite_map = sprite_map
