from pacman.engine.components.component import Component
from pacman.engine.components.entity import Entity
from pacman.services.ghosts_behavior.behavior import Behavior


class Target(Component):
    def __init__(
        self,
        cell_size: float,
        target: Entity,
        maze_size: tuple[int, int],
        maze: list[list[int]],
        behavior_class: type[Behavior],
    ):
        self.behavior = behavior_class
        self.cell_size = cell_size
        self.target = target
        self.maze_size = maze_size
        self.maze = maze
