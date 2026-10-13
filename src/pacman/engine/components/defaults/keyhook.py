import pyray as pr

from ..component import Component
from .direction import Dir


class KeyHook(Component):
    """Map keyboard keys to movement directions."""

    def __init__(self, keys: dict[pr.KeyboardKey, Dir]) -> None:
        """Create a keyboard mapping.

        Args:
            keys: Mapping from keyboard keys to directions.
        """
        self.keys = keys
