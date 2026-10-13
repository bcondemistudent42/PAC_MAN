from ..component import Component
from .direction import Dir


class Intention(Component):
    """Store the next direction requested by an entity."""

    def __init__(self, direction: Dir) -> None:
        """Create an intention component.

        Args:
            direction: Initially requested direction.
        """
        self.direction = direction
