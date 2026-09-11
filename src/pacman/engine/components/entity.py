from typing import TypeVar, cast
from pacman.engine.components.component import Component


T = TypeVar("T", bound=Component)

class Entity:
    def __init__(self, id: str):
        self.id = id
        self.components: dict[type[Component], Component] = {}

    def add_component(self, component: Component):
        self.components[type(component)] = component

    def get_component(self, component: type[T]) -> T:
        return cast(T, self.components[component])
