import time

from pacman.engine.components.defaults.position import Position
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.respawn import Respawn
from pacman.game.components.scared import Scared
from pacman.game.resources import PacmanResources


class SuperPacugumSystem(System):
    def __init__(self, resources: PacmanResources):
        super().__init__([Scared])
        self.resources = resources
        self.events = self.resources.events
        self.last_time_eaten = 0
        self.cooldown = 6  # arbitrary value to adapt

    def run(self) -> None:
        if self.resources.frozen:
            return

        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "super_pacgum"]
            ):
                pacman = event.entities["pacman"]
                if pacman.get_component(Dead).dead or pacman.get_component(Position).x == pacman.get_component(Respawn).x or pacman.get_component(Position).y == pacman.get_component(Respawn).y:
                    return
                self.last_time_eaten = time.time()
                for entt in self.subscribers:
                    if not entt.get_component(Dead).dead:
                        entt.get_component(Scared).scared = True
                        entt.get_component(Scared).end_scared = False

        for entt in self.subscribers:
            if time.time() - self.last_time_eaten > self.cooldown:
                entt.get_component(Scared).scared = False
                entt.get_component(Scared).end_scared = False
            elif time.time() - self.last_time_eaten > 4:
                if entt.get_component(Scared).scared:
                    entt.get_component(Scared).end_scared = True
                    entt.get_component(Scared).scared = False 

# bug when a ghost have been eaten right after scared, he still gets the end sacred

# entt.get_component(Dead).dead or entt.get_component(Scared).scared or 