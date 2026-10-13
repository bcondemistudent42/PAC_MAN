from pacman.engine.components.component import Component


class Scared(Component):
    """Track whether a ghost is frightened and its ending animation."""

    def __init__(self, sprites: list[str]) -> None:
        """Create a scared-state component.

        Args:
            sprites: Sprite names used while the entity is scared.
        """
        self.scared = False
        self.end_scared = False
        self.sprites = sprites
