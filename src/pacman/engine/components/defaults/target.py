from pacman.engine.components.component import Component
from pacman.engine.components.entity import Entity
from pacman.services.solver import BlinkyBehavior


class Target(Component):
    def __init__(
        self,
        cell_size: float,
        target: Entity,
        maze_size: tuple[int, int],
        maze: list[list[int]],
        behavior_class: type = BlinkyBehavior,
    ):
        self.behavior = behavior_class
        self.cell_size = cell_size
        self.target_coord = target
        self.maze_size = maze_size
        self.maze = maze
