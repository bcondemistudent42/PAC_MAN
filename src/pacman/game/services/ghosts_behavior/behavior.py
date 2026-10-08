from abc import ABC, abstractmethod
from random import randint

from pacman.engine.components.defaults.position import Position
from pacman.engine.components.entity import Entity
from pacman.game.services.ghosts_behavior.astar import Astar
from pacman.game.systems.target import GhostState


class Behavior(ABC):
    def __init__(
        self,
        ghost: Entity,
        pacman: Entity,
        cell_size: float,
        maze_size: tuple[int, int],
        maze: list[list[int]],
        corner: tuple[int, int],
    ):
        self.ghost = ghost
        self.pacman = pacman
        self.maze_size = maze_size
        self.maze = maze
        self.cell_size = cell_size
        self.corner = corner
        self.solver = Astar(self.maze_size, self.maze)
        self.fisrt_scatter = True

    @abstractmethod
    def find_pacman(self, state: GhostState) -> list | None:
        pass

    @staticmethod
    def pixel_to_matrix(
        coord: tuple[int | float, int | float], cell_size: float
    ) -> tuple[int, int]:
        x, y = coord
        return (int(x // cell_size), int(y // cell_size))

    def scared_behavior(self):
        x_ghost = self.ghost.get_component(Position).x
        y_ghost = self.ghost.get_component(Position).y
        x_ghost_graph, y_ghost_graph = self.pixel_to_matrix(
            (x_ghost, y_ghost), self.cell_size
        )

        self.ghost_coord = (x_ghost_graph, y_ghost_graph)

        return self.solver.find_road(
            (x_ghost_graph, y_ghost_graph), self.corner
        )

    def scatered_behavior(self):
        x_ghost = self.ghost.get_component(Position).x
        y_ghost = self.ghost.get_component(Position).y
        x_ghost_graph, y_ghost_graph = self.pixel_to_matrix(
            (x_ghost, y_ghost), self.cell_size
        )

        self.ghost_coord = (x_ghost_graph, y_ghost_graph)

        if self.fisrt_scatter:
            self.x_rdn = (randint(0, self.maze_size[0]- 1))
            self.y_rdn = (randint(0, self.maze_size[0]- 1))
            self.fisrt_scatter = False

        return self.solver.find_road(
            (x_ghost_graph, y_ghost_graph), (self.x_rdn, self.y_rdn)
        )

