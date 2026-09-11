from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.components.entity import Entity


def make_death(entity: Entity, death_sprites: list[str]):
    velocity_component = entity.get_component(Velocity)
    sprite_component = entity.get_component(Sprites)

    velocity_component.x = 0
    velocity_component.y = 0
    # sprite_component.sprite_index = 0
    sprite_component.sprites = death_sprites
    # to see which respawn to put and freeze the position


class DeathSprites:
    def __init__(self) -> None:
        self.GHOSTS = ["blue-ghost-1", "blue-ghost-2", "white-ghost-1", "white-ghost-2"]
        self.PACMAN = [
            "pacman-dead-1",
            "pacman-dead-2",
            "pacman-dead-3",
            "pacman-dead-4",
            "pacman-dead-5",
            "pacman-dead-6",
            "pacman-dead-7",
            "pacman-dead-8",
            "pacman-dead-9",
            "pacman-dead-10",
            "pacman-dead-11",
        ]
