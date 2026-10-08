import pyray as pr

from pacman.engine.components.defaults import Sprites
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.scared import Scared
from pacman.game.resources import PacmanResources
from pacman.game.services.death import DeathSprites


class ScoreSystem(System):
    def __init__(self, resources: PacmanResources):
        self.subscribers = []
        self.resources = resources
        self.events = resources.events
        self.required_components = None

    def run(self):
        pr.draw_text(f"Score: {self.resources.score}", 1600, 100, 60, pr.WHITE)
        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "ghost"]
            ):
                ghost = event.entities["ghost"]

                if ghost.get_component(Scared).scared:
                    self.resources.score += self.resources.data_score.point_per_ghosts
            elif isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "pacgum"]
            ):
                self.resources.score += self.resources.data_score.point_per_pacgum

            elif isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "super_pacgum"]
            ):
                self.resources.score += self.resources.data_score.points_per_super_pacgum
