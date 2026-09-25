from pacman.engine.components.component import Component
from pacman.engine.components.entity import Entity


class Target(Component):
    def __init__(
        self,
        target: Entity,
        maze_size: tuple[int, int],
        maze: list[list[int]],
        behavior,
    ):
        self.behavior = behavior
        self.target = target
        self.maze_size = maze_size
        self.maze = maze
