from abc import ABC, abstractmethod

from ..components import Component, Entity


class System(ABC):
    """Base class for systems operating on subscribed entities."""

    def __init__(self, components: list[type[Component]]):
        """Create a system requiring a set of component types.

        Args:
            components: Component types required by subscribed entities.
        """
        self.subscribers: list[Entity] = []
        self.required_components: list[type[Component]] | None = components

    def subscribe(self, entity: Entity) -> None:
        """Subscribe an entity after validating its required components.

        Args:
            entity: Entity to subscribe.

        Raises:
            ValueError: If a required component is missing.
        """
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
                f"{type(self).__name__}: "
                f"missing required component(s): {missing}."
            )

        self.subscribers.append(entity)

    def unsubscribe(self, entity: Entity) -> None:
        """Remove an entity from the system's subscribers.

        Args:
            entity: Entity to remove.
        """
        self.subscribers.remove(entity)

    @abstractmethod
    def run(self) -> None:
        """Process the system's subscribed entities for one update."""
        ...
