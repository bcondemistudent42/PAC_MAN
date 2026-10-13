from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.keyhook import KeyHook
from pacman.engine.components.entity import Entity
from pacman.engine.systems.defaults.key import KeyPressEvent
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.resources import PacmanResources


class PacmanIntentionSystem(System):
    """Translate player key events into movement intentions."""

    def __init__(self, resources: PacmanResources) -> None:
        """Create a player intention system."""
        super().__init__([Intention, KeyHook])
        self.resources = resources

    def subscribe(self, entity: Entity) -> None:
        """Subscribe entities that expose a keyboard hook."""
        if entity.check_component(KeyHook):
            self.subscribers.append(entity)

    def run(self) -> None:
        """Apply queued key events to living controllable entities."""
        if self.resources.frozen:
            return

        for event in self.resources.events.events:
            if not isinstance(event, KeyPressEvent):
                continue

            for subscriber in self.subscribers:
                if (
                    subscriber.check_component(Dead)
                    and subscriber.get_component(Dead).dead
                ):
                    continue
                key_hook = subscriber.get_component(KeyHook)
                target_direction = key_hook.keys.get(event.key)

                if target_direction is not None:
                    subscriber.get_component(
                        Intention
                    ).direction = target_direction
