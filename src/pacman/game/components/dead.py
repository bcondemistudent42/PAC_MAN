from pacman.engine.components.component import Component
from pacman.engine.components.defaults.direction import Dir


class Dead(Component):
    def __init__(self, sprites: dict[Dir, list[str]]) -> None:
        self.dead = False
        self.ready_respawn = False
        self.dead_time = 0.0
        self.dead_cooldown = 2.0
        self.sprites = sprites
        self.eaten = False
