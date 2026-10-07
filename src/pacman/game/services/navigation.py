from pacman.engine.services.navigation import NavigationService
from pacman.game.services.maps import PacmanCell


class PacmanNavigationService(NavigationService):
    def __init__(self, matrix, tile_size):
        self.matrix = matrix
        self.tile_size = tile_size

    def is_walkable(self, x: int, y: int) -> bool:
        if 0 <= y < len(self.matrix) and 0 <= x < len(self.matrix[0]):
            return self.matrix[y][x] != PacmanCell.WALL
        return False
