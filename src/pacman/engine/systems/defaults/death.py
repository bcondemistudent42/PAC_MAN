from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.respawn import Respawn
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources
from pacman.services.death import DeathSprites


class DeathSystem(System):
    def __init__(self, ressources: Ressources):
        super().__init__([Collision, Hitbox])
        self.ressources = ressources
        self.events = self.ressources.events
        self.lives = ressources.data_score.lives
        self.entt_to_resp = []

    def run(self) -> None:

        check = True
        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "ghost"]
            ):
                pacman = event.entities["pacman"]
                pacman.get_component(Sprites).sprites = DeathSprites().PACMAN
                index = pacman.get_component(Sprites).sprite_index
                if self.lives == 0:
                    raise ValueError("Oh NO NO NO NO NO you LOOSED")
                if (index < len(DeathSprites().PACMAN) - 1):
                    for entt in self.entt_to_resp:
                        entt.get_component(Velocity).speed = 0
                    return
                pacman.get_component(Sprites).sprites = pacman.get_component(Direction).sprite_map[Dir.RIGHT]
                pacman.get_component(Direction).direction = Dir.RIGHT
                pacman.get_component(Intention).direction = Dir.RIGHT
                pacman.get_component(Sprites).sprite_index = 0
                for entt in self.entt_to_resp:
                    entt.get_component(Velocity).speed = entt.get_component(Respawn).speed
                    entt.get_component(Position).x = entt.get_component(Respawn).x
                    entt.get_component(Position).y = entt.get_component(Respawn).y

                if check:
                    self.lives -= 1
                    check = False

                # handle death properly, freeze all ghost and make pacman_respawn at center
                # make respawn all ghost at their corners
                # to see the choices depending on the self.lives rest

            elif isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "pacgum"]
            ):
                cell = event.entities["pacgum"]
                cell.get_component(Sprites).sprites = ["no-pacgum-cell"]
                cell.components.pop(Collision, None)
                cell.components.pop(Hitbox, None)

