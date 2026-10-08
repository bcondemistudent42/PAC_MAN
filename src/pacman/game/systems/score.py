from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.systems.defaults.collision import CollisionEvent
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
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

                    event.entities["ghost"].get_component(Sprites).display = False
                    self.resources.freeze(1)

            elif isinstance(event, CollisionEvent) and all(
                e in event.entities for e in ["pacman", "super_pacgum"]
            ):
                self.resources.score += self.resources.data_score.points_per_super_pacgum

