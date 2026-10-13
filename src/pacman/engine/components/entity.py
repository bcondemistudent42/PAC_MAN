from typing import TypeVar, cast

from .component import Component

T = TypeVar("T", bound=Component)


class Entity:
    """Represent a game object composed of typed components."""

    def __init__(self, id: str) -> None:
        """Create an entity with a stable identifier.

        Args:
            id: Identifier used to distinguish the entity.
        """
        self.id = id
        self.components: dict[type[Component], Component] = {}

    def add_component(self, component: Component | list[Component]) -> None:
        """Attach one component or a list of components to the entity.

        Args:
            component: Component instance or component instances to attach.

        Raises:
            TypeError: If ``component`` is not a component or list of them.
        """
        if isinstance(component, list):
            for each_comp in component:
                self.add_component(each_comp)
            return

        if not isinstance(component, Component):
            err = "Expected a Component instance",
            "or a list of Component instances, "
            raise TypeError(
                err,
                f"got {type(component).__name__}."
            )

        self.components[type(component)] = component

    def get_component(self, component: type[T]) -> T:
        """Return a component by its concrete type.

        Args:
            component: Type of component to retrieve.

        Returns:
            The stored component cast to the requested type.
        """
        return cast(T, self.components[component])

    def check_component(self, component: type[Component]) -> bool:
        """Return whether the entity has a component of the given type."""
        return bool(self.components.get(component))
