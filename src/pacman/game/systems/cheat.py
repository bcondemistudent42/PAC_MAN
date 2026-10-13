import pyray as pr

from pacman.engine.systems.system import System
from pacman.game.components.scared import Scared
from pacman.game.resources import PacmanResources


class CheatSystem(System):
    """Toggle gameplay cheats controlled by keyboard shortcuts."""

    def __init__(self, resources: PacmanResources) -> None:
        """Create a cheat system using shared Pac-Man resources."""
        super().__init__([Scared])
        self.resources = resources

    def run(self) -> None:
        """Toggle cheats when their keyboard shortcuts are pressed."""
        if self.resources.cheat_corner and pr.is_key_pressed(
            pr.KeyboardKey.KEY_C
        ):
            self.resources.cheat_corner = False
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_C):
            self.resources.cheat_corner = True

        if self.resources.cheat_scared and pr.is_key_pressed(
            pr.KeyboardKey.KEY_S
        ):
            self.resources.cheat_scared = False
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_S):
            self.resources.cheat_scared = True
