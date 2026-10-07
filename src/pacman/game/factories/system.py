from pacman.engine.engine import GameEngine
from pacman.engine.systems.defaults.collision import CollisionSystem
from pacman.engine.systems.defaults.key import KeySystem
from pacman.engine.systems.defaults.movement import MovementSystem
from pacman.engine.systems.defaults.sprite import SpriteSystem
from pacman.engine.systems.defaults.time import TimeSystem
from pacman.game.resources import resources
from pacman.game.systems.death import DeathSystem
from pacman.game.systems.direction_sprite import DirectionSpriteSystem
from pacman.game.systems.pacgum import PacgumSystem
from pacman.game.systems.pacman_intention import PacmanIntentionSystem
from pacman.game.systems.respawn_ghost import RespawnGhostSystem
from pacman.game.systems.score import ScoreSystem
from pacman.game.systems.super_pacgum_system import SuperPacugumSystem
from pacman.game.systems.target import TargetSystem


class SystemFactory:
    def __init__(self, resources: resources, engine: GameEngine) -> None:
        self.resources = resources
        self.engine = engine

    def create_all(self) -> None:
        self.engine.add_system([
            CollisionSystem(self.resources),
            MovementSystem(self.resources),
            SpriteSystem(self.resources),
            KeySystem(self.resources),
            PacmanIntentionSystem(self.resources),
            TargetSystem(self.resources),
            DeathSystem(self.resources),
            PacgumSystem(self.resources),
            TimeSystem(self.resources),
            SuperPacugumSystem(self.resources),
            DirectionSpriteSystem(self.resources),
            RespawnGhostSystem(self.resources),
            ScoreSystem(self.resources)
        ])

