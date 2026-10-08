import time
from collections.abc import Callable

from pacman.engine.engine import GameEngine
from pacman.engine.scenes.scene import Scene
from pacman.engine.services.sprites import SpriteService
from pacman.game.factories.ghost import GhostFactory
from pacman.game.factories.pacman import PacmanFactory
from pacman.game.factories.system import SystemFactory
from pacman.game.resources import PacmanResources
from pacman.game.scenes.gameover import GameOverScene
from pacman.game.services.maps import PacmanMap
from pacman.game.services.navigation import PacmanNavigationService
from pacman.game.services.parser import Parser
from pacman.game.settings import GameSettings
from pacman.game.systems.death import GameOverEvent


class GameScene(Scene):
    def __init__(
        self,
        settings: GameSettings,
        sprite_service: SpriteService,
        game_data: Parser,
        level: int = 1,
    ):
        self.settings = settings
        self.level = level
        self.sprite_service = sprite_service
        self.game_data = game_data
        self.freeze_duration = 0
        self.frozen_at = time.time()

    def enter(self, engine: GameEngine) -> None:
        self.map_service = PacmanMap(
            engine, self.settings, seed=self.game_data.seed
        )
        
        navigation_service = PacmanNavigationService(
            self.map_service.logic_matrix, self.map_service.TILE_SIZE
        )

        self.resources = PacmanResources(
            events=engine.events,
            data_score=self.game_data,
            scale=self.settings.scale,
            matrix=self.map_service.get_map_matrix(),
            sprite_service=self.sprite_service,
            navigation_service=navigation_service,
            pacgum_count=0,
            level_max_time=self.game_data.level_max_time,
            freeze=self.freeze,
            frozen=False
        )

        SystemFactory(self.resources, engine, self.settings).create_all()
        self.map_service.generate_map()
        self.resources.pacgum_count = self.map_service.pacgum_count
        
        pacman = PacmanFactory(self.settings, engine).create()
        GhostFactory(
            settings=self.settings,
            maze=self.map_service.map,
            pacman=pacman,
            engine=engine,
            resources=self.resources,
        ).create_all()

    def update(self, engine: GameEngine) -> None | Scene:
        if (
            self.resources.frozen
            and (time.time() - self.frozen_at >= self.freeze_duration)
        ):
            self.resources.frozen = False
            self.freeze_callback()

        try:
            event = next(filter(lambda e: isinstance(e, GameOverEvent), engine.events.events))            
            from pacman.game.scenes.menu import MenuScene

            return GameOverScene(
                self.settings,
                event.score,
                MenuScene(
                    self.settings, self.sprite_service
                ),
                self.sprite_service
            )

        except StopIteration:
            engine.events.drain()

        if self.resources.pacgum_count == 0:
            return GameScene(
                self.settings,
                self.sprite_service,
                self.game_data,
                level=self.level + 1,
            )
        return None

    def render(self, engine: GameEngine) -> None:
        for system in engine.systems:
            system.run()

    def exit(self, engine: GameEngine) -> None:
        engine.clear()

    def freeze(
        self,
        freeze_duration: float,
        callback: Callable
    ) -> None:
        self.resources.frozen = True
        self.freeze_duration = freeze_duration
        self.frozen_at = time.time()
        self.freeze_callback = callback
