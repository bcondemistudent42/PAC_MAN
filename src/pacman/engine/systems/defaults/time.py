import time

import pyray as pr

from ...engine.resources import Resources
from ...engine.systems.system import System


class TimeSystem(System):
    def __init__(self, ressources: Resources):
        self.start_time = time.time()
        self.time_left = 0
        self.ressources = ressources
        self.required_components = None

    def run(self) -> None:
        level_max_time = self.ressources.level_max_time
        if level_max_time is None:
            raise RuntimeError(
                "Level time limit is unavailable. Configure it before "
                "running TimeSystem."
            )

        self.time_left = round(
            level_max_time - abs(self.start_time - time.time()),
            2,
        )
        pr.draw_text(
            f"Time remaining: {self.time_left}", 1600, 200, 50, pr.WHITE
        )
        if self.time_left < 0:
            raise TimeoutError("The level time limit has expired.")
