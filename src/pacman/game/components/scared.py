from pacman.engine.components.component import Component


class Scared(Component):
    def __init__(self, sprites: list[str]) -> None:
        self.scared = False
        self.end_scared = False
        self.sprites = sprites
