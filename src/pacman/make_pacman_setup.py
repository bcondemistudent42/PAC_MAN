import random

import mazegenerator as mg

from pacman.engine.ecs import Entity, Map, Position, Sprite, Velocity
from pacman.engine.systems.systems import MovementSystem, SpriteSystem
from pacman.services.sprites import SpriteService, config


class PacmanSetup:

    def __init__(self):
        pass

    @staticmethod
    def make_entities_lvl() -> None:
        output = []

        output.append(
            PacmanSetup.create_level(True)
        )
        for i in range(10):
            output.append(
                PacmanSetup.create_level()
            )
        return output

            # to see how to handle sprite for the map later

    @staticmethod
    def create_level(first_level: bool= False):
        my_maze = mg.MazeGenerator()
        if first_level:
            my_maze.generate(seed=42)
        else:
            my_maze.generate(seed=random.randint(0, 10000))

        level_entity = Entity("level_0")
        map_component = Map(my_maze.maze)
        level_entity.add_component(map_component)
        return level_entity

    # def create_pacman_entities():
    #     sprite_system = SpriteSystem({SpriteService: SpriteService("sprites/spritesheet.png", config)})
    #     movement_system = MovementSystem(None)


    #     p = Position(10, 10)
    #     v = Velocity(0, 0)
    #     spr = Sprite("pacman-right-1")

    #     pac_man = Entity("pac_man")
    #     pac_man.add_component(Position)
    #     pac_man.add_component(Velocity)
    #     pac_man.add_component(Sprite)

    #     sprite_system.subscribe(pac_man)
    #     movement_system.subscribe(pac_man)
    #     return pac_man

    # def create_ghosts_entity():
