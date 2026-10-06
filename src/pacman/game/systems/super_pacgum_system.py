
import time

from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.scared import Scared
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
                for entt in self.subscribers:
                    if not entt.get_component(Dead).dead:
                        entt.get_component(Scared).scared = True

        if time.time() - self.last_time_eaten > self.cooldown:
            for entt in self.subscribers:
                entt.get_component(Scared).scared = False
                entt.get_component(Scared).end_scared = False
        elif time.time() - self.last_time_eaten > 6:
           for entt in self.subscribers:
                entt.get_component(Scared).end_scared = True
                entt.get_component(Scared).scared = False

