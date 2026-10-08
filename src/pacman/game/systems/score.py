from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.components.entity import Entity
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.ghost_score import GhostScore
from pacman.game.resources import PacmanResources


class ScoreSystem(System):
    def __init__(self, resources: PacmanResources):
        super().__init__([Velocity])
        self.resources = resources
        self.events = resources.events
        self.required_components = None

    def run(self):
        if self.resources.frozen:
            return

        eaten_ghosts: list[tuple[Entity, Entity]] = []

        for event in self.events.events:
            if isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "pacgum"]
            ):
                self.resources.score += self.resources.data_score.point_per_pacgum

            elif isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "ghost"]
            ):
                if (
                    event.entities["ghost"].get_component(Dead).dead
                    and not event.entities["ghost"].get_component(Dead).eaten
                ):
                    self.resources.score += self.resources.data_score.point_per_ghosts
                    event.entities["ghost"].get_component(Dead).eaten = True
                    event.entities["pacman"].get_component(Sprites).display = False
                    event.entities["ghost"].get_component(Sprites).display = False
                    event.entities["ghost"].get_component(GhostScore).display = True
                    eaten_ghosts.append(
                        (event.entities["pacman"], event.entities["ghost"])
                    )


            elif isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "super_pacgum"]
            ):
                self.resources.score += self.resources.data_score.points_per_super_pacgum

        if eaten_ghosts:
            def on_unfreeze() -> None:
                for pacman, ghost in eaten_ghosts:
                    pacman.get_component(Sprites).display = True
                    ghost.get_component(Sprites).display = True
                    ghost.get_component(GhostScore).display = False

            self.resources.freeze(1, on_unfreeze)

