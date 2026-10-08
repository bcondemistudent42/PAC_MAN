import time

import pyray as pr

from pacman.engine.systems.system import System
from pacman.game.resources import resources


class TimeSystem(System):
    def __init__(self, ressources: resources):
        self.start_time = time.time()
        self.time_left = 0
        self.ressources = ressources
        self.required_components = None

    def run(self) -> None:
        self.time_left = round(
            self.ressources.data_score.level_max_time
            - abs(self.start_time - time.time()),
            2,
        )
        pr.draw_text(
            f"Time remaining: {self.time_left}", 1600, 200, 50, pr.WHITE
        )
        if self.time_left < 0:
            raise TimeoutError("The level time limit has expired.")
