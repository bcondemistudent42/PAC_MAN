from pacman.engine.components.component import Component
from pacman.engine.components.defaults.direction import Dir


class Dead(Component):
    def __init__(self, sprites: dict[Dir, list[str]]) -> None:
        self.dead = False
        self.sprites = sprites
