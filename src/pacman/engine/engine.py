import pyray as pr

from pacman.engine.components import Entity
from pacman.engine.systems import System
from pacman.services.parser import parse


class GameEngine:
    def __enter__(self):
        pr.init_window(self.window_width, self.window_height, "PACMAN DEBUG")
        my_monitor = pr.get_current_monitor()
        monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
        monitor_h = int(pr.get_monitor_height(my_monitor) / 4) * 3
        pr.set_window_size(monitor_w, monitor_h)
        pr.set_target_fps(60)

        self.data_user = parse()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pr.close_window()

    def __init__(self):
        self.entities: list[Entity] = []
        self.systems: list[System] = []
        self.window_width = 2000
        self.window_height = 1500

    def add_system(self, system: list[System] | System) -> None:
        if isinstance(system, System):
            self.systems.append(system)
        elif isinstance(system, list):
            self.systems.extend(system)
        else:
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
                required in entity.components for required in system.required_components
            ):
                system.subscribe(entity)

    def run(self):
        while not pr.window_should_close():
            pr.begin_drawing()
            pr.draw_fps(1000, 10)
            pr.clear_background(pr.BLACK)

            for system in self.systems:
                system.run()

            pr.end_drawing()
