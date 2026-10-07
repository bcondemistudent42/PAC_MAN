import pyray as pr

from pacman.engine.components import Entity
from pacman.engine.events.queue import EventsQueue
from pacman.engine.scenes.scene import Scene
from pacman.engine.systems import System


class GameEngine:
    def __enter__(self):
        pr.init_window(self.window_width, self.window_height, "PACMAN")
        self.monitor_w = self.window_width
        self.monitor_h = self.window_height
        moni = pr.get_current_monitor()
        h = pr.get_monitor_height(moni)
        w = pr.get_monitor_width(moni)
        # pr.set_window_size(monitor_w, monitor_h)
        pr.set_window_position(w // 8, h // 8)
        pr.set_target_fps(60)
        self.scene.enter()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pr.close_window()

    def __init__(
        self,
        scene: Scene,
        window_width: int,
        window_height: int
    ):
        self.entities: list[Entity] = []
        self.systems: list[System] = []
        self.events = EventsQueue()
        self.window_width = window_width
        self.window_height = window_height
        self.scene = scene

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
            raise TypeError(
                "Cannot add this in entities to adapt add entities"
            )

    def add_single_entity(self, entity: Entity) -> None:
        self.entities.append(entity)

        for system in self.systems:
            if not system.required_components:
                continue
            if all(
                required in entity.components for required in system.required_components
            ):
                system.subscribe(entity)

    def run(self):
        while not pr.window_should_close():

            new_scene = self.scene.update()

            if new_scene:
                self.scene.exit()
                self.scene = new_scene
                self.scene.enter()

            pr.begin_drawing()
            pr.clear_background(pr.BLACK)

            self.scene.render(self)

            pr.end_drawing()

            self.events.drain()
