from typing import TypeVar, cast

from .component import Component

T = TypeVar("T", bound=Component)


class Entity:
    def __init__(self, id: str):
        self.id = id
        self.components: dict[type[Component], Component] = {}

    def add_component(self, component: Component | list[Component]):
        if isinstance(component, list):
            for each_comp in component:
                self.add_component(each_comp)
            return

        if not isinstance(component, Component):
            raise TypeError(
                "Expected a Component instance or a list of Component instances, "
                f"got {type(component).__name__}."
            )

        self.components[type(component)] = component

    def get_component(self, component: type[T]) -> T:
        return cast(T, self.components[component])

    def check_component(self, component: type[Component]) -> bool:
        return bool(self.components.get(component))
