from abc import ABC, abstractmethod

from pacman.engine.components.defaults.position import Position
from pacman.engine.components.entity import Entity


class Behavior(ABC):
    def __init__(
        self,
        ghost: Entity,
        pacman: Entity,
        maze_size: tuple[int, int],
        maze: list[list[int]],
    ):
        self.ghost = ghost
        self.pacman = pacman
        self.maze_size = maze_size
        self.maze = maze

        x_ghost = ghost.get_component(Position).x
        y_ghost = ghost.get_component(Position).y
        from pacman.engine.components.defaults.target import Target
        cell_size = ghost.get_component(Target).cell_size

        self.ghost_coord = (self.pixel_to_matrix(
            (x_ghost, y_ghost),
            cell_size)
        )

        x_pacman = pacman.get_component(Position).x
        y_pacman = pacman.get_component(Position).y

        self.pacman_coord = (self.pixel_to_matrix(
            (x_pacman, y_pacman),
            cell_size)
        )

    @abstractmethod
    def find_pacman(self) -> list | None:
        pass

    @staticmethod
    def pixel_to_matrix(coord: tuple[int | float, int | float], cell_size: float) -> tuple[int, int]:
        x, y = coord
        return (int(x // cell_size), int(y // cell_size))