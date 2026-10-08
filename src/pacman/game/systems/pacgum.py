from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.respawn import Respawn
from pacman.game.resources import PacmanResources


class PacgumSystem(System):
    def __init__(self, resources: PacmanResources):
        super().__init__([Collision, Hitbox])
        self.resources = resources
        self.events = self.resources.events

    def run(self) -> None:
        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "pacgum"]
            ):
                cell = event.entities["pacgum"]
                cell.get_component(Sprites).sprites = ["no-pacgum-cell"]
                cell.components.pop(Collision, None)
                cell.components.pop(Hitbox, None)

            elif (
                isinstance(event, CollisionEvent) and
                all(e in event.entities for e in ["pacman", "super_pacgum"]) and
                not event.entities["pacman"].get_component(Dead).dead
            ):
                pacman = event.entities["pacman"]
                if pacman.get_component(Dead).dead or pacman.get_component(Position).x == pacman.get_component(Respawn).x or pacman.get_component(Position).y == pacman.get_component(Respawn).y:
                    return
                cell = event.entities["super_pacgum"]
                cell.get_component(Sprites).sprite_index = 0
                cell.get_component(Sprites).sprites = ["no-pacgum-cell"]
                cell.components.pop(Collision, None)
                cell.components.pop(Hitbox, None)
