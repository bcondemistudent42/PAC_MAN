
import pyray as pr

from pacman.engine.ecs import Entity
from pacman.engine.systems.systems import System
from pacman.make_pacman_setup import PacmanSetup


class GameEngine:

    def __enter__(self):

        pr.init_window(800, 450 , "PACMAN")
        my_monitor = pr.get_current_monitor()
        monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
        monitor_h = int(pr.get_monitor_height(my_monitor) / 4) * 3
        pr.set_window_size(monitor_w, monitor_h)
        pr.set_target_fps(60)
        # to clean in a function pr

        # self.entities.extend(
        #     PacmanSetup.make_entities_lvl()
        # )
        # self.entities.append(
        #     PacmanSetup.create_pacman_entities()
        # )
        # to think later review with anselme

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
        # here the game really starts
        while not pr.window_should_close():
            pr.begin_drawing()

            pr.clear_background(pr.BLACK)

            for system in self.systems:
                system.run()

            pr.end_drawing()