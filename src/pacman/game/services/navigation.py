from pacman.engine.services.navigation import NavigationService
from pacman.game.services.maps import PacmanCell


class PacmanNavigationService(NavigationService):
    """Navigate the logical Pac-Man map matrix."""

    def __init__(
        self, matrix: list[list[PacmanCell]], tile_size: float
    ) -> None:
        """Create a navigation service for a map matrix.

        Args:
            matrix: Logical map cells.
            tile_size: Size of one logical tile in pixels.
        """
        self.matrix = matrix
        self.tile_size = tile_size

    def is_walkable(self, x: int, y: int) -> bool:
        """Return whether the given map cell is inside the map and open."""
        if 0 <= y < len(self.matrix) and 0 <= x < len(self.matrix[0]):
            return self.matrix[y][x] != PacmanCell.WALL
        return False
