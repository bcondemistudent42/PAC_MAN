from abc import ABC, abstractmethod


class NavigationService(ABC):
    @abstractmethod
    def is_walkable(self, x: int, y: int) -> bool:
        pass
