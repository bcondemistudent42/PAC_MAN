from types import TracebackType

import pyray as pr

from .components import Entity
from .events.queue import EventsQueue
from .scenes.scene import Scene
from .systems import System


class GameEngine:
    """Coordinate entities, systems, events, scenes, and rendering."""

    def __enter__(self) -> "GameEngine":
        """Enter the current scene and return the engine."""
        self.scene.enter(self)

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the current scene and close the rendering window."""
        self.scene.exit(self)
        pr.close_window()

    def __init__(
        self, scene: Scene, window_width: int, window_height: int
    ) -> None:
        """Create an engine with an initial scene and window dimensions.

        Args:
            scene: Scene active when the engine starts.
            window_width: Window width in pixels.
            window_height: Window height in pixels.
        """
        self.entities: list[Entity] = []
        self.systems: list[System] = []
        self.events = EventsQueue()
        self.window_width = window_width
        self.window_height = window_height
        self.scene = scene

    def add_system(self, system: list[System] | System) -> None:
        """Register one system or a list of systems.

        Args:
            system: System or systems to register.

        Raises:
            TypeError: If the value is neither a system nor a list.
        """
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
        """Register one entity or a list of entities.

        Args:
            entity: Entity or entities to register.

        Raises:
            TypeError: If the value is neither an entity nor a list.
        """
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
        """Register an entity and subscribe it to matching systems."""
        self.entities.append(entity)

        for system in self.systems:
            if not system.required_components:
                continue
            if all(
                required in entity.components
                for required in system.required_components
            ):
                system.subscribe(entity)

    def run(self) -> None:
        """Run the main update, scene, and rendering loop."""
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
        """Remove all entities, subscribers, systems, and queued events."""
        self.entities.clear()
        for system in self.systems:
            if system.subscribers is None:
                continue
            system.subscribers.clear()
        self.systems.clear()
        self.events.drain()
