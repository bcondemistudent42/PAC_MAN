import pyray as pr

from .components import Entity
from .events.queue import EventsQueue
from .scenes.scene import Scene
from .systems import System


class GameEngine:
    def __enter__(self):
        self.scene.enter(self)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.scene.exit(self)
        pr.close_window()

    def __init__(self, scene: Scene, window_width: int, window_height: int):
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
            raise TypeError(
                "add_system() expects a System or a list of Systems, "
                f"got {type(system).__name__}."
            )

    def add_entities(self, entity: Entity | list[Entity]) -> None:
        if isinstance(entity, Entity):
            self.add_single_entity(entity)
        elif isinstance(entity, list):
            for e in entity:
                self.add_single_entity(e)
        else:
            raise TypeError(
                "add_entities() expects an Entity or a list of Entities, "
                f"got {type(entity).__name__}."
            )

    def add_single_entity(self, entity: Entity) -> None:
        self.entities.append(entity)

        for system in self.systems:
            if not system.required_components:
                continue
            if all(
                required in entity.components
                for required in system.required_components
            ):
                system.subscribe(entity)

    def run(self):
        while not pr.window_should_close():
            new_scene = self.scene.update(self)

            if new_scene:
                self.scene.exit(self)
                self.scene = new_scene
                self.scene.enter(self)

            pr.begin_drawing()
            pr.clear_background(pr.BLACK)

            self.scene.render(self)

            pr.end_drawing()

    def clear(self) -> None:
        self.entities.clear()
        for system in self.systems:
            system.subscribers.clear()
        self.events.drain()
