from pacman.engine.components.component import Component


class Sprites(Component):
    def __init__(self, sprites: list[str], cooldown: float):
        self.sprites = sprites
        self.sprite_index = 0
        self.frame: float = 0
        self.cooldown = cooldown
