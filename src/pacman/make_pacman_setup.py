import random

import mazegenerator as mg

from pacman.engine.ecs import Entity, Map


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
