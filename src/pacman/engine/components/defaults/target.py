from pacman.engine.components.component import Component
from pacman.ghosts_solver import BlinkyBehavior


class Target(Component):
    def __init__(
        self,
        entity_coord: tuple[int, int],
        target_coord: tuple[int, int],
        maze_size: tuple[int, int],
        maze: list[list[int]]
    ):
    # to define special behavior later for each ghosts
        self.behavior = BlinkyBehavior
        self.entity_coord = entity_coord
        self.target_coord = target_coord
        self.maze_size = maze_size
        self.maze = maze