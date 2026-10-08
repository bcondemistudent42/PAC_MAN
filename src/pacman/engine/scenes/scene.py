from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..engine import GameEngine


class Scene(ABC):
    @abstractmethod
    def update(self, engine: GameEngine) -> None | Scene: ...

    @abstractmethod
    def enter(self, engine: GameEngine) -> None: ...

    @abstractmethod
    def exit(self, engine: GameEngine) -> None: ...

    @abstractmethod
    def render(self, engine: GameEngine) -> None: ...
