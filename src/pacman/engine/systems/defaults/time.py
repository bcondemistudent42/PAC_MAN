import time

import pyray as pr

from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources


class TimeSystem(System):
    def __init__(self, ressources: Ressources):
        self.start_time = time.time()
        self.time_left = 0
        self.ressources = ressources

    def run(self) -> None:
        self.time_left = round(abs(self.start_time - time.time()), 2)
        pr.draw_text(f"Time remaining: {self.time_left}", 1700, 550, 100, pr.WHITE)
        if self.time_left >= self.ressources.data_score.level_max_time:
            raise (ValueError("Time exceeded"))