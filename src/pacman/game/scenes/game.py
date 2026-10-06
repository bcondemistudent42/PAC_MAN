from enum import Enum
import sys

from pacman.engine.engine import GameEngine
from pacman.engine.scenes.scene import Scene
from pacman.game.settings import GameSettings
import pyray as pr


class GameScene(Scene):
    def __init__(
        self,
        settings: GameSettings
    ):
        self.settings = settings

    def enter(self):
        ...

    def update(self) -> None:
        ...

    def render(self, engine: GameEngine) -> None:
        for system in engine.systems:
            system.run()


    def exit(self):
        ...
