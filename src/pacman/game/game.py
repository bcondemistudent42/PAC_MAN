from pacman.engine.components.defaults.position import Position
from pacman.engine.components.entity import Entity
from pacman.engine.engine import GameEngine
from pacman.engine.systems.defaults import (
    CollisionSystem,
    KeySystem,
    MovementSystem,
    PacmanIntentionSystem,
    SpriteSystem,
)
from pacman.engine.systems.defaults.time import TimeSystem
from pacman.game.factories.ghost import GhostFactory
from pacman.game.factories.pacman import PacmanFactory
from pacman.game.factories.system import SystemFactory
from pacman.game.resources import resources
from pacman.game.services.maps import PacmanMap
from pacman.game.services.sprites import (
    SpriteService,
    config,
    config_spritesheet_2,
)
from pacman.game.settings import GameSettings
from pacman.game.systems.death import DeathSystem
from pacman.game.systems.direction_sprite import DirectionSpriteSystem
from pacman.game.systems.pacgum import PacgumSystem
from pacman.game.systems.respawn_ghost import RespawnGhostSystem
from pacman.game.systems.score import ScoreSystem
from pacman.game.systems.super_pacgum_system import SuperPacugumSystem
from pacman.game.systems.target import TargetSystem


class PacmanGame:
    def __init__(self, engine: GameEngine, settings: GameSettings):
        self.engine = engine
        self.pacman: Entity | None = None
        self.settings = settings
        self.resources = resources(
            self.engine.events,
            scale=self.settings.scale,
        )
        self.map_service = PacmanMap(self.engine, self.settings)

    def start_game(self):
        self.resources.matrix = self.matrix
        self.resources.sprite_service = self.sprite_service
        self.resources.scale = self.settings.scale
        self.engine.run()

    def systems_init(self) -> None:
        systems_factory = SystemFactory(self.resources, self.engine)
        systems_factory.create_all()

    def services_init(self) -> None:
        sprite_sheet = "sprites/spritesheet.png"
        self.sprite_service = SpriteService(sprite_sheet, config)
        self.sprite_service.add_spritesheet(
            "sprites/creeper.png", config_spritesheet_2)

    def make_full_setup(self):
        self.services_init()
        self.systems_init()
        self.map_service.generate_map()
        self.matrix = self.map_service.get_map_matrix()
        self.create_movable_entities()

    def create_movable_entities(self) -> None:
        pacman = PacmanFactory(self.settings, self.engine).create()
        GhostFactory(
            settings=self.settings,
            maze=self.map_service.map,
            pacman=pacman,
            engine=self.engine,
        ).create_all()
