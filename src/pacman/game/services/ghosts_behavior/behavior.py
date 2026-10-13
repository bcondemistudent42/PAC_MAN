from abc import ABC, abstractmethod

from pacman.engine.components.defaults.position import Position
from pacman.engine.components.entity import Entity
from pacman.game.services.ghosts_behavior.astar import Astar
from pacman.game.systems.target import GhostState


class Behavior(ABC):
    """Base class for ghost target-selection strategies."""

    def __init__(
        self,
        ghost: Entity,
        pacman: Entity,
        cell_size: float,
        maze_size: tuple[int, int],
        maze: list[list[int]],
        corner: tuple[int, int],
    ):
        """Create a behavior strategy for a ghost and maze.

        Args:
            ghost: Ghost controlled by the behavior.
            pacman: Pac-Man entity being targeted.
            cell_size: Size of one logical cell in pixels.
            maze_size: Maze dimensions.
            maze: Maze wall representation.
            corner: Ghost home corner used for scatter behavior.
        """
        self.ghost = ghost
        self.pacman = pacman
        self.maze_size = maze_size
        self.maze = maze
        self.cell_size = cell_size
        self.corner = corner
        self.solver = Astar(self.maze_size, self.maze)

    @abstractmethod
    def find_pacman(
        self, state: GhostState
    ) -> list[tuple[int, int]] | None:
        """Return a route toward Pac-Man for the current ghost state."""
        pass

    @staticmethod
    def pixel_to_matrix(
        coord: tuple[int | float, int | float], cell_size: float
    ) -> tuple[int, int]:
        """Convert pixel coordinates to logical cell coordinates."""
        x, y = coord
        return (int(x // cell_size), int(y // cell_size))

    def scared_behavior(self) -> list[tuple[int, int]] | None:
        """Return a route toward the ghost's home corner."""
        x_ghost = self.ghost.get_component(Position).x
        y_ghost = self.ghost.get_component(Position).y
        x_ghost_graph, y_ghost_graph = self.pixel_to_matrix(
            (x_ghost, y_ghost), self.cell_size
        )

        self.ghost_coord = (x_ghost_graph, y_ghost_graph)

        return self.solver.find_road(
            (x_ghost_graph, y_ghost_graph), self.corner
        )

    def find_scatter(
        self, scatter_point: tuple[int, int]
    ) -> list[tuple[int, int]] | None:
        """Return a route from the ghost to a scatter point."""
        x_ghost = self.ghost.get_component(Position).x
        y_ghost = self.ghost.get_component(Position).y
        x_ghost_graph, y_ghost_graph = self.pixel_to_matrix(
            (x_ghost, y_ghost), self.cell_size
        )

        self.ghost_coord = (x_ghost_graph, y_ghost_graph)

        return self.solver.find_road(
            (x_ghost_graph, y_ghost_graph), scatter_point
        )
