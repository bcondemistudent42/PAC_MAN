import time

from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.ghost_score import GhostScore
from pacman.game.components.respawn import Respawn
from pacman.game.components.scared import Scared
from pacman.game.resources import PacmanResources


# class CheatSystem(System):
    # def __init__(self, resources: PacmanResources):
        # super().__init__()
        # self.resources = resources

    # def run(self) -> None:
        # if 