import pyray as pr

from pacman.engine.components.defaults import Position, Sprites
from pacman.game.components.scared import Scared
from pacman.engine.systems.defaults.collision import CollisionEvent, CollisionSystem
from pacman.engine.systems.system import System
from pacman.game.resources import resources


class ScoreSystem(System):
    def __init__(self, resources: resources):
        self.resources = resources
        self.events = resources.events
        self.required_components = None
        self.score = 0

    def run(self):

        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "ghost"]
            ):
                # TODO case when pacman dies
                self.score += self.resources.data_score.point_per_ghosts

            elif isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "pacgum"]
            ):
                self.score += self.resources.data_score.point_per_pacgum
        pr.draw_text(f"Score: {self.score}", 1700, 250, 20, pr.WHITE)