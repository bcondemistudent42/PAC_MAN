from __future__ import annotations

from typing import TYPE_CHECKING

from pacman.engine.components.component import Component
from pacman.engine.components.entity import Entity

if TYPE_CHECKING:
    from pacman.game.services.ghosts_behavior.behavior import Behavior


class Target(Component):
    """Store a ghost behavior and its current scatter target."""

    def __init__(
        self,
        target: Entity,
        maze_size: tuple[int, int],
        maze: list[list[int]],
        behavior: Behavior,
        scatter_point: tuple[int, int],
    ) -> None:
        """Create a targeting component.

        Args:
            target: Entity targeted by the behavior.
            maze_size: Maze dimensions in cells.
            maze: Maze wall representation.
            behavior: Strategy used to calculate a route.
            scatter_point: Current scatter destination.
        """
        self.behavior = behavior
        self.target = target
        self.maze_size = maze_size
        self.maze = maze
        self.scatter_point = scatter_point
