from pacman.engine.engine import GameEngine
from pacman.engine.scenes.scene import Scene
from pacman.engine.services.sprites import SpriteService
from pacman.game.factories.ghost import GhostFactory
from pacman.game.factories.pacman import PacmanFactory
from pacman.game.factories.system import SystemFactory
from pacman.game.scenes.gameover import GameOverScene
from pacman.game.services.maps import PacmanMap
from pacman.game.services.navigation import PacmanNavigationService
from pacman.game.settings import GameSettings
from pacman.game.resources import PacmanResources
from pacman.game.systems.death import GameOverEvent


import pyray as pr

class GameScene(Scene):
    def __init__(
        self,
        settings: GameSettings,
        sprite_service: SpriteService,
        level: int = 1
    ):
        self.settings = settings
        self.level = level
        self.sprite_service = sprite_service

    def enter(self, engine: GameEngine) -> None:
        self.map_service = PacmanMap(engine, self.settings)
        
        navigation_service = PacmanNavigationService(
            self.map_service.logic_matrix, self.map_service.TILE_SIZE
        )
        
        self.resources = PacmanResources(
            events=engine.events,
            scale=self.settings.scale,
            matrix=self.map_service.get_map_matrix(),
            sprite_service=self.sprite_service,
            navigation_service=navigation_service
        )
        
        SystemFactory(self.resources, engine, self.settings).create_all()
        
        self.map_service.generate_map()
        
        pacman = PacmanFactory(self.settings, engine).create()
        GhostFactory(
            settings=self.settings,
            maze=self.map_service.map,
            pacman=pacman,
            engine=engine,
        ).create_all()

    def update(self, engine: GameEngine) -> None | Scene:
        try:
            event = next(filter(lambda e: isinstance(e, GameOverEvent), engine.events.events))            
            from pacman.game.scenes.menu import MenuScene

            return GameOverScene(
                self.settings,
                event.score,
                MenuScene(self.settings, self.sprite_service),
                self.sprite_service
            )
        
        except StopIteration:
            engine.events.drain()
            
        return None

    def render(self, engine: GameEngine) -> None:
        for system in engine.systems:
            system.run()

    def exit(self, engine: GameEngine) -> None:
        engine.clear()