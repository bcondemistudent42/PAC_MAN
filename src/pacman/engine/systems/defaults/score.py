import pyray as pr

from pacman.engine.components.defaults import Position, Sprites
from pacman.engine.components.defaults.scared import Scared
from pacman.engine.components.defaults.score import Score
from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources


class ScoreSystem(System):
    def __init__(self, ressources: Ressources):
        super().__init__([Score])
        self.ressources = ressources

    def run(self):
        pass