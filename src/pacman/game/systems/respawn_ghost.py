import time

from pacman.engine.components.defaults.direction import Direction
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.respawn import Respawn
from pacman.game.components.scared import Scared
from pacman.game.resources import resources


class RespawnGhostSystem(System):
    def __init__(self, resources: resources):
        super().__init__([Respawn, Dead, Position, Velocity, Sprites])
        self.resources = resources

    def run(self) -> None:
        for sub in self.subscribers:
            if sub.id == "pac_man":
                continue
            elif sub.get_component(Dead).ready_respawn:
                sub.get_component(Dead).dead_time = time.time()
                sub.get_component(Dead).ready_respawn = False
            elif time.time() - sub.get_component(Dead).dead_time >= sub.get_component(Dead).dead_cooldown and sub.get_component(Dead).dead_time != 0:
                print("Testing")
                sub.get_component(Dead).dead_time = 0.0
                sub.get_component(Scared).scared = False
                sub.get_component(Scared).end_scared = False
                sub.get_component(Dead).ready_respawn = False
                sub.get_component(Dead).dead = False

                sub.get_component(Velocity).speed = sub.get_component(Respawn).speed
                sub.get_component(Sprites).sprites = sub.get_component(Direction).sprite_map[sub.get_component(Direction).direction]
