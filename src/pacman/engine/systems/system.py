from abc import ABC, abstractmethod

from ..components import Component, Entity


class System(ABC):
    def __init__(self, components: list[type[Component]]):
        self.subscribers: list[Entity] = []
        self.required_components: list[type[Component]] | None = components

    def subscribe(self, entity: Entity):
        if not self.required_components:
            return
        missing_components = [
            component.__name__
            for component in self.required_components
            if component not in entity.components
        ]
        if missing_components:
            missing = ", ".join(missing_components)
            raise ValueError(
                f"Cannot subscribe entity {entity.id!r} to "
                f"{type(self).__name__}: missing required component(s): {missing}."
            )

        self.subscribers.append(entity)

    def unsubscribe(self, entity: Entity):
        self.subscribers.remove(entity)

    @abstractmethod
    def run(self) -> None: ...
