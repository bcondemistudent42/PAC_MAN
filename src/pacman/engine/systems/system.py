from abc import ABC, abstractmethod

from pacman.engine.components import Component, Entity


class System(ABC):
    def __init__(self, components: list[type[Component]]):
        self.subscribers: list[Entity] = []
        self.required_components: list[type[Component]] | None = components

    def subscribe(self, entity: Entity):
        if not self.required_components:
            return
        for component in self.required_components:
            if not component in entity.components:
                raise ValueError("A definir")

        self.subscribers.append(entity)

    def unsubscribe(self, entity: Entity):
        self.subscribers.remove(entity)

    @abstractmethod
    def run(self) -> None: ...
