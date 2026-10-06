from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.direction import Direction
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.respawn import Respawn
from pacman.game.resources import resources


class RespawnGhostSystem(System):
    def __init__(self, resources: resources):
        super().__init__([Respawn, Dead, Position, Velocity, Sprites])
        self.resources = resources

    def run(self) -> None:
        for sub in self.subscribers:
            if sub.id == "pac_man":
                continue
            if sub.get_component(Dead).ready_respawn:
                sub.get_component(Position).x = sub.get_component(Respawn).x
                sub.get_component(Position).y = sub.get_component(Respawn).y
                sub.get_component(Velocity).speed = sub.get_component(Respawn).speed
                sub.get_component(Sprites).sprites = sub.get_component(Direction).sprite_map[sub.get_component(Direction).direction]
