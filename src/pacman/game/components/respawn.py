from pacman.engine.components.component import Component


class Respawn(Component):
    """Store an entity's respawn coordinates and restored speed."""

    def __init__(self, x: float, y: float, speed: float) -> None:
        """Create a respawn component.

        Args:
            x: Horizontal respawn coordinate.
            y: Vertical respawn coordinate.
            speed: Speed restored on respawn.
        """
        self.x = x
        self.y = y
        self.speed = speed
