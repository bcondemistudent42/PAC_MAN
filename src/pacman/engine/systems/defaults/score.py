import pyray as pr

from pacman.engine.components.defaults import Position, Sprites
from pacman.engine.components.defaults.scared import Scared
from pacman.engine.systems.defaults.collision import CollisionEvent, CollisionSystem
from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources
from pacman.services.death import DeathSprites


class ScoreSystem(System):
    def __init__(self, ressources: Ressources):
        self.ressources = ressources
        self.events = ressources.events
        self.required_components = None
        self.score = 0

    def run(self):

        pr.draw_text(f"Score: {self.score}", 1700, 250, 100, pr.WHITE)
        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "ghost"]
            ):
                pacman = event.entities["pacman"]
                if pacman.get_component(Sprites).sprites != DeathSprites().PACMAN:
                    return
            elif isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "pacgum"]
            ):
                self.score += self.ressources.data_score.point_per_pacgum