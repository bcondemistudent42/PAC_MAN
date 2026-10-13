from ..component import Component


class Position(Component):
    """Store an entity's position in pixels."""

    def __init__(self, x: float, y: float) -> None:
        """Create a position component.

        Args:
            x: Horizontal coordinate.
            y: Vertical coordinate.
        """
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """Return the position formatted as a coordinate pair."""
        return f"({self.x}, {self.y})"
