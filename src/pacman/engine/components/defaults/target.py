from pacman.engine.components.component import Component
from pacman.engine.components.entity import Entity
from pacman.services.solver import BlinkyBehavior


class Target(Component):
    def __init__(
        self,
        entity_coord: tuple[int, int],
        target: Entity,
        maze_size: tuple[int, int],
        maze: list[list[int]],
        behavior_class: type = BlinkyBehavior,
    ):
        # to define special behavior later for each ghosts
        self.behavior = behavior_class
        self.entity_coord = entity_coord
        self.target_coord = target
        self.maze_size = maze_size
        self.maze = maze
