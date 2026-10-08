import time

from pacman.game.resources import PacmanResources
from pacman.game.systems.death import GameOverEvent

from ...engine.systems.system import System


class TimeSystem(System):
    def __init__(self, resources: PacmanResources):
        self.subscribers = []
        self.start_time = time.time()
        self.time_left = 0
        self.resources = resources
        self.required_components = None
        self.events = self.resources.events

    def run(self) -> None:
        if self.resources.frozen:
            return

        level_max_time = self.resources.level_max_time
        if level_max_time is None:
            raise RuntimeError(
                "Level time limit is unavailable. Configure it before "
                "running TimeSystem."
            )

        self.time_left = round(
            level_max_time - abs(self.start_time - time.time()),
            2,
        )
        self.resources.time_left = self.time_left
        if self.time_left < 0:
            self.events.push(GameOverEvent(self.resources.score))
