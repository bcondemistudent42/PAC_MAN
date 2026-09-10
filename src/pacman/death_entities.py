from enum import Enum

from pacman.engine.ecs import Entity, Sprites, Velocity


def make_death(entity: Entity, death_sprites: list[str]):
    entity.components[Velocity].x = 0
    entity.components[Velocity].y = 0
    entity.components[Sprites].sprites_animation = death_sprites


class DeathSprites(Enum):

    GHOSTS = [
        "blue-ghost-1",
        "blue-ghost-2",
        "white-ghost-1",
        "white-ghost-2"
    ]

    PACMAN = [
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
                "pacman-dead-11"
    ]