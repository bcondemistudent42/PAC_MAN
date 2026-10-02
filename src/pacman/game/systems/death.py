from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.is_dying import Isdying
from pacman.engine.components.defaults.keyhook import KeyHook
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.respawn import Respawn
from pacman.game.resources import resources
from pacman.game.services.death import DeathSprites


class DeathSystem(System):
    def __init__(self, resources: resources):
        super().__init__([Collision, Hitbox])
        self.resources = resources
        self.events = self.resources.events
        self.lives = resources.data_score.lives
        self.entt_to_resp = []
        self.first_go = True

# TODO BUG when pressing keys in the death animation of pac_man

    def run(self) -> None:

        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "ghost"]
            ):
                pacman = event.entities["pacman"]
                pacman.get_component(Sprites).sprites = DeathSprites().PACMAN
                index = pacman.get_component(Sprites).sprite_index

                if self.lives == 1:
                    raise ValueError("Oh NO NO NO NO NO you LOOSED")
                if (index < len(DeathSprites().PACMAN) - 1):
                    pacman.get_component(Isdying).dying = True
                    if self.first_go:
                        for entt in self.entt_to_resp:
                            if not entt.check_component(KeyHook):
                                entt.get_component(Sprites).sprites = []
                            entt.get_component(Velocity).speed = 0
                    self.first_go = False
                    return

                self.first_go = True
                pacman.get_component(Sprites).sprites = pacman.get_component(Direction).sprite_map[Dir.RIGHT]
                pacman.get_component(Direction).direction = Dir.RIGHT
                pacman.get_component(Intention).direction = Dir.RIGHT
                pacman.get_component(Sprites).sprite_index = 0
                pacman.get_component(Isdying).dying = False

                for entt in self.entt_to_resp:
                    entt.get_component(Velocity).speed = entt.get_component(Respawn).speed
                    entt.get_component(Position).x = entt.get_component(Respawn).x
                    entt.get_component(Position).y = entt.get_component(Respawn).y
                    entt.get_component(Sprites).sprites = entt.get_component(Direction).sprite_map[Dir.RIGHT]

                self.lives -= 1
