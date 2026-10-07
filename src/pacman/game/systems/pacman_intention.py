from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.keyhook import KeyHook
from pacman.engine.components.entity import Entity
from pacman.engine.systems.defaults.key import KeyPressEvent
from pacman.engine.systems.system import System
from pacman.game.resources import resources


class PacmanIntentionSystem(System):
    def __init__(self, resources: resources):
        super().__init__([Intention, KeyHook])
        self.resources = resources

    def subscribe(self, entity: Entity):
        if entity.check_component(KeyHook):
            self.subscribers.append(entity)

    def run(self) -> None:
        for event in self.resources.events.events:
            if not isinstance(event, KeyPressEvent):
                continue

            for subscriber in self.subscribers:
                key_hook = subscriber.get_component(KeyHook)
                target_direction = key_hook.keys.get(event.key)

                if target_direction is not None:
                    subscriber.get_component(
                        Intention
                    ).direction = target_direction
