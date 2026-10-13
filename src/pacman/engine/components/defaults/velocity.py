from ..component import Component


class Velocity(Component):
    """Store an entity's current and base movement speed."""

    def __init__(self, speed: float) -> None:
        """Create a velocity component.

        Args:
            speed: Initial movement speed in pixels per update.
        """
        self.speed = speed
        self.base_speed = speed
