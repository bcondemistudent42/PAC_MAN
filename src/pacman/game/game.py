from pacman.engine.components.entity import Entity
from pacman.engine.engine import GameEngine
from pacman.engine.services.sprites import SpriteService
from pacman.game.factories.ghost import GhostFactory
from pacman.game.factories.pacman import PacmanFactory
from pacman.game.factories.system import SystemFactory
from pacman.game.resources import PacmanResources
from pacman.game.services.maps import PacmanMap
from pacman.game.services.navigation import PacmanNavigationService
from pacman.game.factories.sprites import SpriteFactory
from pacman.game.settings import GameSettings


class PacmanGame:
    def __init__(self, engine: GameEngine, settings: GameSettings):
        self.engine = engine
        self.pacman: Entity | None = None
        self.settings = settings
        self.resources = PacmanResources(
            self.engine.events,
            scale=self.settings.scale,
        )
        self.map_service = PacmanMap(self.engine, self.settings)

    def start_game(self):
        self.resources.matrix = self.matrix
        self.resources.scale = self.settings.scale
        self.engine.run()

    def systems_init(self) -> None:
        systems_factory = SystemFactory(self.resources, self.engine)
        systems_factory.create_all()

    def services_init(self) -> None:
        sprite_sheet = "sprites/spritesheet.png"
        main_sprites, map_sprites = SpriteFactory().create()
        self.sprite_service = SpriteService(sprite_sheet, main_sprites)
        self.sprite_service.add_spritesheet(
            "sprites/creeper.png", map_sprites
        )
        self.navigation_service = PacmanNavigationService(
            self.map_service.logic_matrix,
            self.map_service.TILE_SIZE,
        )
        self.resources.navigation_service = self.navigation_service
        self.resources.sprite_service = self.sprite_service

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
