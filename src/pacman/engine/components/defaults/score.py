from pacman.engine.components.component import Component
from pacman.game.ressources import Ressources


class Score(Component):
    def __init__(self, ressources: Ressources):
        self.score = 0
        self.ressources = ressources
