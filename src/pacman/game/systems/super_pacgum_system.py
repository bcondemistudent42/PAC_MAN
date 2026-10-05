
import time

from pacman.engine.components.defaults.direction import Dir
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.scared import Scared
from pacman.game.dead import Dead
from pacman.game.resources import resources


class SuperPacugumSystem(System):
    def __init__(self, resources: resources):
        super().__init__([Scared])
        self.resources = resources
        self.events = self.resources.events
        self.last_time_eaten = 0
        self.cooldown = 8  #arbitrary value to adapt

    def run(self) -> None:
        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "super_pacgum"]
            ):
                self.last_time_eaten = time.time()
                # print(self.entt_adapt_behavior)
                for entt in self.subscribers:
                    entt.get_component(Scared).scared = True
                    entt.get_component(Sprites).sprite_index = 0
                    entt.get_component(Sprites).sprites = entt.get_component(Scared).sprites[0:2]

            if time.time() - self.last_time_eaten > self.cooldown:
                for entt in self.subscribers:
                    # entt.get_component(Sprites).sprite_index = 0
                    # entt.get_component(Sprites).sprites = entt.get_component().sprites
                    entt.get_component(Scared).scared = False
            elif time.time() - self.last_time_eaten > 2:
                for entt in self.subscribers:
                    entt.get_component(Sprites).sprites = entt.get_component(Sprites).sprites


