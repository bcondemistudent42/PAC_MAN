from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.hitbox import Hitbox
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

    def run(self) -> None:
        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "ghost"]
            ):
                pacman = event.entities["pacman"]
                pacman.get_component(Sprites).sprites = DeathSprites().PACMAN
                pacman.get_component(Velocity).speed = 0

                self.events.events.remove(event)

            elif isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "pacgum"]
            ):
                cell = event.entities["pacgum"]
                cell.get_component(Sprites).sprites = ["no-pacgum-cell"]
                cell.components.pop(Collision, None)
                cell.components.pop(Hitbox, None)

                self.events.events.remove(event)
