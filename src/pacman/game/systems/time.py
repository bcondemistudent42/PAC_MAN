import time

from pacman.game.resources import PacmanResources
from pacman.game.systems.death import GameOverEvent
import pyray as pr

from ...engine.systems.system import System


class TimeSystem(System):
    """Track the level timer and emit game-over events when it expires."""

    def __init__(self, resources: PacmanResources) -> None:
        """Create a level timer system."""
        self.subscribers = []
        self.resources = resources
        self.time_left: float = resources.level_max_time
        self.required_components = None
        self.events = self.resources.events

    def run(self) -> None:
        """Update the remaining time and emit a timeout event if needed."""
        if self.resources.frozen:
            return

        level_max_time = self.resources.level_max_time
        if level_max_time is None:
            raise RuntimeError(
                "Level time limit is unavailable. Configure it before "
                "running TimeSystem."
            )

        self.time_left -= pr.get_frame_time()
        self.resources.time_left = self.time_left
        if self.time_left < 0:
            self.events.push(GameOverEvent(self.resources.score))
