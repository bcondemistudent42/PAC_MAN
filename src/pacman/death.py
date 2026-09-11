from enum import Enum

from pacman.engine.ecs import Entity, Sprites, Velocity


def make_death(entity: Entity, death_sprites: list[str]):
    velocity_component = entity.get_component(Velocity)
    sprite_component = entity.get_component(Sprites)
    
    velocity_component.x = 0
    velocity_component.y = 0
    # sprite_component.sprite_index = 0
    sprite_component.sprites = death_sprites
    # to see which respawn to put and freeze the position



class DeathSprites(Enum):

    GHOSTS = (
        "blue-ghost-1",
        "blue-ghost-2",
        "white-ghost-1",
        "white-ghost-2"
    )

<<<<<<< HEAD
    PACMAN = (
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
    )
=======
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
>>>>>>> 1abaaa35c787c691af50873e48e6f7d544c54336
