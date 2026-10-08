from pacman.engine.engine import GameEngine
from pacman.engine.systems.defaults.collision import CollisionSystem
from pacman.engine.systems.defaults.key import KeySystem
from pacman.engine.systems.defaults.movement import MovementSystem
from pacman.engine.systems.defaults.sprite import SpriteSystem
from pacman.game.resources import PacmanResources
from pacman.game.settings import GameSettings
from pacman.game.systems.death import DeathSystem
from pacman.game.systems.direction_sprite import DirectionSpriteSystem
from pacman.game.systems.pacgum import PacgumSystem
from pacman.game.systems.intention import PacmanIntentionSystem
from pacman.game.systems.respawn_ghost import RespawnGhostSystem
from pacman.game.systems.score import ScoreSystem
from pacman.game.systems.super_pacgum import SuperPacugumSystem
from pacman.game.systems.target import TargetSystem
from pacman.game.systems.time import TimeSystem


class SystemFactory:
    def __init__(
        self,
        resources: PacmanResources,
        engine: GameEngine,
        settings: GameSettings,
    ) -> None:
        self.resources = resources
        self.engine = engine
        self.settings = settings

    def create_all(self) -> None:
        self.engine.add_system(
            [
                CollisionSystem(self.resources),
                MovementSystem(self.resources),
                SpriteSystem(self.resources),
                KeySystem(self.resources),
                PacmanIntentionSystem(self.resources),
                TargetSystem(
                    self.resources,
                    chase_duration=self.settings.chase_duration,
                    scatter_duration=self.settings.scatter_duration,
                ),
                DeathSystem(self.resources),
                PacgumSystem(self.resources),
                TimeSystem(self.resources),
                SuperPacugumSystem(self.resources),
                DirectionSpriteSystem(self.resources),
                RespawnGhostSystem(self.resources),
                ScoreSystem(self.resources),
            ]
        )
