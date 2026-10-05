
from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.keyhook import KeyHook
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.respawn import Respawn
from pacman.game.components.scared import Scared
from pacman.game.resources import resources


class DeathSystem(System):
    def __init__(self, resources: resources):
        super().__init__([Collision, Hitbox])
        self.resources = resources
        self.events = self.resources.events
        self.lives = resources.data_score.lives
        self.entt_to_resp = []
        self.first_go = True

    def run(self) -> None:

        if self.first_go is False:
            index = self.pacman.get_component(Sprites).sprite_index
            if index < len(self.pacman.get_component(Sprites).sprites) - 1:
                return
            self.pacman.get_component(Dead).dead = False
            if self.lives == 1:
                raise ValueError("Oh NO NO NO NO NO you LOOSED")

            self.pacman.get_component(Sprites).sprite_index = 0
            self.pacman.get_component(Sprites).sprites = self.pacman.get_component(Direction).sprite_map[Dir.RIGHT]
            self.pacman.get_component(Direction).direction = Dir.RIGHT
            self.pacman.get_component(Intention).direction = Dir.RIGHT
            for entt in self.entt_to_resp:
                entt.get_component(Velocity).speed = entt.get_component(Respawn).speed
                entt.get_component(Position).x = entt.get_component(Respawn).x
                entt.get_component(Position).y = entt.get_component(Respawn).y
                entt.get_component(Sprites).display = True
                entt.get_component(Sprites).sprite_index = 0
            self.lives -= 1
            self.first_go = True
            self.pacman.get_component(Dead).dead = False

        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "ghost"]
            ):
                pacman = event.entities["pacman"]
                self.pacman = pacman
                scared = event.entities["ghost"].get_component(Scared).scared
                end_scared = event.entities["ghost"].get_component(Scared).end_scared
                if scared:
                    ghost = event.entities["ghost"]
                    ghost.get_component(Sprites).sprite_index = 0

                if not scared and not end_scared:
                    pacman.get_component(Dead).dead = True
                    for entt in self.entt_to_resp:
                        if not entt.check_component(KeyHook):
                            entt.get_component(Sprites).display = False
                            entt.get_component(Sprites).sprite_index = 0
                        entt.get_component(Velocity).speed = 0
                    self.first_go = False
