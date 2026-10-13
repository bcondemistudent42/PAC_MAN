from ..component import Component


class Sprites(Component):
    """Store animation frames and their display state."""

    def __init__(
        self, sprites: list[str], cooldown: float | None = None
    ) -> None:
        """Create a sprite animation component.

        Args:
            sprites: Ordered sprite names used as animation frames.
            cooldown: Seconds between frame changes, if animated.
        """
        self.sprites = sprites
        self.sprite_index = 0
        self.frame: float = 0
        self.cooldown = cooldown
        self.display = True
