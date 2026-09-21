import pyray as pr

from pacman.engine.components import Entity
from pacman.engine.systems import System
from pacman.parser import parse


class GameEngine:
    def __enter__(self):
        pr.init_window(self.window_width, self.window_height, "PACMAN DEBUG")
        my_monitor = pr.get_current_monitor()
        monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
        monitor_h = int(pr.get_monitor_height(my_monitor) / 4) * 3
        pr.set_window_size(monitor_w, monitor_h)
        pr.set_target_fps(60)

        # to clean in a function pr to see how to do ask anselme

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
            # print(f"{system}, {type(system)}")
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
        # here the game really starts
        i = 0
        while not pr.window_should_close():
            i += 1
            pr.begin_drawing()
            pr.draw_fps(1000, 10)

            pr.clear_background(pr.BLACK)

            for system in self.systems:
                system.run()

            # to clean all this only for testing
            # TODO a proper dislay or render maze
            # my_monitor = pr.get_current_monitor()
            # monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
            # monitor_h = int(pr.get_monitor_height(my_monitor) / 4) * 3
            # rect_in_w = (monitor_w * 6) // 10
            # rect_in_h = (monitor_h * 9) // 10
            # x_in = (monitor_w - rect_in_w) // 2
            # y_in = (monitor_h - rect_in_h) // 2

            # margin = 10
            # radius = 20

            # rect_out_w = rect_in_w + (margin * 2)
            # rect_out_h = rect_in_h + (margin * 2)
            # x_out = x_in - margin
            # y_out = y_in - margin

            # from pacman.ft_pyray import FtPyray
            # FtPyray.ft_draw_rounded_rectangle(
            #     (x_in, y_in), rect_in_w, rect_in_h, radius, pr.BLUE
            # )
            # FtPyray.ft_draw_rounded_rectangle(
            #     (x_out, y_out), rect_out_w, rect_out_h, radius, pr.BLUE
            # )

            pr.end_drawing()
