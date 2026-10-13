from ..component import Component


class Hitbox(Component):
    """Define the collision rectangle relative to an entity position."""

    def __init__(
        self,
        width: float,
        height: float,
        padding_x: float = 0,
        padding_y: float = 0,
    ) -> None:
        """Create a hitbox.

        Args:
            width: Hitbox width in pixels.
            height: Hitbox height in pixels.
            padding_x: Horizontal offset from the entity position.
            padding_y: Vertical offset from the entity position.
        """
        self.width = width
        self.height = height
        self.padding_x = padding_x
        self.padding_y = padding_y
