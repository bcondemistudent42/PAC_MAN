from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..engine import GameEngine


class Scene(ABC):
    """Define the lifecycle contract for an engine scene."""

    @abstractmethod
    def update(self, engine: GameEngine) -> None | Scene:
        """Advance the scene and optionally return its replacement."""
        ...

    @abstractmethod
    def enter(self, engine: GameEngine) -> None:
        """Initialize scene state when it becomes active."""
        ...

    @abstractmethod
    def exit(self, engine: GameEngine) -> None:
        """Release scene state when it stops being active."""
        ...

    @abstractmethod
    def render(self, engine: GameEngine) -> None:
        """Render the current scene state."""
        ...
