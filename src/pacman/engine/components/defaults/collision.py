from ..component import Component


class Collision(Component):
    """Identify an entity for collision detection."""

    def __init__(self, tag: str) -> None:
        """Create a collision component.

        Args:
            tag: Name used to classify the entity in collision events.
        """
        self.tag = tag
