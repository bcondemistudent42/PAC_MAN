
import pyray as pr

from pacman.engine.ecs import Entity
from pacman.engine.systems.systems import System


class GameEngine:
    def __enter__(self):
        pr.init_window(1200, 800, "PACMAN DEBUG")
        # my_monitor = pr.get_current_monitor()
        # monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
        # monitor_h = int(pr.get_monitor_height(my_monitor) / 4) * 3
        # pr.set_window_size(monitor_w, monitor_h)
        pr.set_target_fps(60)
        # to clean in a function pr to see how to do ask anselme

        from pacman.pacman_game import PacmanGame
        setup = PacmanGame(self)
        setup.make_full_setup()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pr.close_window()

    def __init__(self, name: str):
        self.name = name
        self.entities: list[Entity] = []
        self.systems: list[System] = []

    def add_system(self, system: list[System] | System) -> None:
        if isinstance(system, System):
            self.systems.append(system)
        elif isinstance(system, list):
            self.systems.extend(system)
        else:
            print(f"{system}, {type(system)}")
            raise TypeError("Cannot add this in system to adapt add system")

    def add_entities(self, entity: Entity | list[Entity]) -> None:
        if isinstance(entity, Entity):
            self.add_single_entity(entity)
        elif isinstance(entity, list):
            for e in entity:
                self.add_single_entity(e)
        else:
            raise TypeError("Cannot add this in entities to adapt add entities")

    def add_single_entity(self, entity: Entity) -> None:
        self.entities.append(entity)

        for system in self.systems:
            if all(
                required in entity.components
                for required in system.required_components
            ):
                system.subscribe(entity)

    def run(self):
        # here the game really starts
        i = 0
        while not pr.window_should_close():
            i += 1
            pr.begin_drawing()

            pr.clear_background(pr.BLACK)

            for system in self.systems:
                system.run()

            pr.end_drawing()
