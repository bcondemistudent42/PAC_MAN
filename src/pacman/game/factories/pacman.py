from pacman.engine.components.entity import Entity
from pacman.engine.engine import GameEngine


class PacmanFactory:
    def __init__(
        self, scale: float, maze: list[list[int]], pacman: Entity, engine: GameEngine
    ) -> None:
        self.SCALE = scale
        self.maze = maze
        self.pacman = pacman
        self.engine = engine
