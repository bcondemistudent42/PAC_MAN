
import pyray as pr

from pacman.engine.ecs import Entity
from pacman.engine.systems.systems import System


class GameEngine:

    def __enter__(self):

        pr.init_window(800, 450 , "PACMAN")
        my_monitor = pr.get_current_monitor()
        monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
        monitor_h = int(pr.get_monitor_height(my_monitor) / 4) * 3
        pr.set_window_size(monitor_w, monitor_h)
        pr.set_target_fps(60)
        # to clean in a function pr

        from pacman.make_pacman_setup import PacmanSetup
        setup = PacmanSetup(self)
        setup.make_full_setup()
        # TODO:
        # Create all the ghosts entities

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pr.close_window()


    def __init__(self, name: str):
        self.name = name
        self.entities: list[Entity] = []
        self.systems: list[System] = []

    def add_system(self, system: list[System] | System):
        if isinstance(system, System):
            self.systems.append(system)
        elif type(system) == list:
            self.systems.extend(system)
        else:
            print(f"{system}, {type(system)}")
            raise ValueError("Cannot add this in system to adapt add system")

    def add_entities(self, entity: Entity):
        if type(entity) == Entity:
            self.entities.append(entity)
        elif type(entity) == list:
            self.entities.extend(entity)
        else:
            raise ValueError("Cannot add this in entities to adapt add entities")

    def run(self):
        # here the game really starts
        while not pr.window_should_close():
            pr.begin_drawing()

            pr.clear_background(pr.BLACK)

            for system in self.systems:
                system.run()

            pr.end_drawing()