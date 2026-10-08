from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.keyhook import KeyHook
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.components.entity import Entity
from pacman.engine.events.event import Event
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.respawn import Respawn
from pacman.game.components.scared import Scared
from pacman.game.resources import PacmanResources
import pyray as pr 


class GameOverEvent(Event):
    def __init__(self, score: int) -> None:
        self.score = score


class DeathSystem(System):
    def __init__(self, resources: PacmanResources):
        super().__init__(
            [Collision, Hitbox, Dead, Respawn, Position, Velocity, Sprites]
        )
        self.resources = resources
        self.events = self.resources.events
        self.pacman: Entity | None = None
        self.is_dying = False

    def run(self) -> None:
        if self.resources.sprite_service:
            for i in range(self.resources.data_score.lives):
                pr.draw_texture_ex(
                    self.resources.sprite_service.get_sprite("pacman-right-2"),
                    pr.Vector2(1600 + 100 * i, 400),
                    0.0,
                    self.resources.scale,
                    pr.WHITE,
                )

        if self.is_dying:
            if self.pacman is None:
                return

            sprites_comp = self.pacman.get_component(Sprites)
            if sprites_comp.sprite_index < len(sprites_comp.sprites) - 1:
                return

            self.pacman.get_component(Dead).dead = False
            if self.resources.data_score.lives <= 0:
                self.events.push(GameOverEvent(self.resources.score))

            sprites_comp.sprite_index = 0
            sprites_comp.sprites = self.pacman.get_component(
                Direction
            ).sprite_map[Dir.RIGHT]
            self.pacman.get_component(Direction).direction = Dir.RIGHT
            self.pacman.get_component(Intention).direction = Dir.RIGHT

            for entt in self.subscribers:
                if entt.check_component(Respawn):
                    respawn = entt.get_component(Respawn)
                    entt.get_component(Velocity).speed = respawn.speed
                    entt.get_component(Position).x = respawn.x
                    entt.get_component(Position).y = respawn.y
                    entt.get_component(Sprites).display = True

            self.resources.data_score.lives -= 1
            self.is_dying = False
            return

        for event in self.events.events:
            if not isinstance(event, CollisionEvent):
                continue

            if not all(e in event.entities for e in ["pacman", "ghost"]):
                continue

            pacman = event.entities["pacman"]
            ghost = event.entities["ghost"]

            if (
                pacman.get_component(Dead).dead
                or ghost.get_component(Dead).dead
            ):
                continue

            scared = ghost.get_component(Scared).scared
            end_scared = ghost.get_component(Scared).end_scared

            if scared or end_scared:
                ghost.get_component(Dead).dead = True
                ghost.get_component(Scared).scared = False
                ghost.get_component(Scared).end_scared = False
            else:
                self.pacman = pacman
                pacman.get_component(Dead).dead = True
                self.is_dying = True

                for entt in self.subscribers:
                    if not entt.check_component(KeyHook):
                        s = entt.get_component(Sprites)
                        s.display = False
                        s.sprite_index = 0
                    entt.get_component(Velocity).speed = 0
                break
