from pacman.engine.components.component import Component


class Scared(Component):
    def __init__(self, scared_sprites: list[str]) -> None:
        self.scared = False
        self.sprites = scared_sprites
