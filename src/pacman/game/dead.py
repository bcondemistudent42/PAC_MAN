from pacman.engine.components.component import Component


class Dead(Component):
    def __init__(self, dead_sprites: list[str]) -> None:
        self.dead = False
        self.sprites = dead_sprites
