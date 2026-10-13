from abc import ABC, abstractmethod


class NavigationService(ABC):
    """Define the interface used to test traversable map cells."""

    @abstractmethod
    def is_walkable(self, x: int, y: int) -> bool:
        """Return whether a map coordinate can be traversed.

        Args:
            x: Horizontal map coordinate.
            y: Vertical map coordinate.

        Returns:
            ``True`` when the coordinate is traversable.
        """
        pass
