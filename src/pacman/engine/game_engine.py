import random

import mazegenerator as mg
import pyray as pr

from pacman.engine.ecs import Entity, Map
from pacman.engine.systems.systems import System


class GameEngine:

    def __enter__(self):

        pr.init_window(800, 450 , "PACMAN")
        my_monitor = pr.get_current_monitor()
        monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
        monitor_h = int(pr.get_monitor_height(my_monitor) / 4) * 3
        pr.set_window_size(monitor_w, monitor_h)
        pr.set_target_fps(60)

        # to create all the maze with entities
        self.make_entities_lvl()
        # make_10_entities_lvl() -> lst and first of them have seed 42
        # the others have random seeds

        # to create all the pacman and ghosts enities
        # to call sprite manager of anselme

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pr.close_window()


    def __init__(self, name: str):
        self.name = name
        self.entities: list[Entity] = []
        self.systems: list[System] = []

    def add_system(self, system: System):
        self.systems.append(system)

    def add_entities(self, entity: Entity):
        self.entities.append(entity)

    def run(self):
        while not pr.window_should_close():
            pr.begin_drawing()

            pr.clear_background(pr.BLACK)

            pr.end_drawing()

    def make_entities_lvl(self) -> None:

        self.entities.append(
            self.create_level(True)
        )

        for i in range(10):
            self.entities.append(
                self.create_level()
            )
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



        # context manager
        # ici que le jeu se lance vrm
