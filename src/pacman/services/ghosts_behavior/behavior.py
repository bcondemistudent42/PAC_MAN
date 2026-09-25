from abc import ABC, abstractmethod

from pacman.engine.components.defaults.position import Position
from pacman.engine.components.entity import Entity
from pacman.services.ghosts_behavior.astar import Astar


class Behavior(ABC):
    def __init__(
        self,
        ghost: Entity,
        pacman: Entity,
        cell_size: float,
        maze_size: tuple[int, int],
        maze: list[list[int]],
    ):
        self.ghost = ghost
        self.pacman = pacman
        self.maze_size = maze_size
        self.maze = maze
        self.cell_size = cell_size
        self.solver = Astar(
            self.maze_size,
            self.maze
        )

    @abstractmethod
    def find_pacman(self) -> list | None:
        pass

    @staticmethod
    def pixel_to_matrix(coord: tuple[int | float, int | float], cell_size: float) -> tuple[int, int]:
        x, y = coord
        return (int(x // cell_size), int(y // cell_size))