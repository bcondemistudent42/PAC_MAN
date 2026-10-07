from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pacman.engine.engine import GameEngine

class Scene(ABC):
    @abstractmethod
    def update(self) -> None | Scene:
        ...

    @abstractmethod
    def enter(self) -> None:
        ...

    @abstractmethod
    def exit(self) -> None:
        ...

    @abstractmethod
    def render(self, engine: GameEngine) -> None:
        ...
