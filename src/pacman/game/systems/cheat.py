
import pyray as pr

from pacman.engine.systems.system import System
from pacman.game.components.scared import Scared
from pacman.game.resources import PacmanResources


class CheatSystem(System):
    def __init__(self, resources: PacmanResources):
        super().__init__([Scared])
        self.resources = resources

    def run(self) -> None:
        if self.resources.cheat_corner and pr.is_key_pressed(pr.KeyboardKey.KEY_C):
            self.resources.cheat_corner = False
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_C):
                self.resources.cheat_corner = True

        if self.resources.cheat_scared and pr.is_key_pressed(pr.KeyboardKey.KEY_S):
            self.resources.cheat_scared = False
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_S):
                self.resources.cheat_scared = True