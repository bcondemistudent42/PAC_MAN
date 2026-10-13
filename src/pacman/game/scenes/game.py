import time
from collections.abc import Callable
from typing import cast

import pyray as pr

from pacman.engine.engine import GameEngine
from pacman.engine.scenes.scene import Scene
from pacman.engine.services.sprites import SpriteService
from pacman.game.factories.ghost import GhostFactory
from pacman.game.factories.pacman import PacmanFactory
from pacman.game.factories.system import SystemFactory
from pacman.game.resources import PacmanResources
from pacman.game.scenes.gameover import GameOverScene
from pacman.game.scenes.win import WinScene
from pacman.game.services.maps import PacmanMap
from pacman.game.services.navigation import PacmanNavigationService
from pacman.game.services.parser import Parser
from pacman.game.settings import GameSettings
from pacman.game.systems.death import GameOverEvent


class GameScene(Scene):
    """Run one playable Pac-Man level."""

    def __init__(
        self,
        settings: GameSettings,
        sprite_service: SpriteService,
        game_data: Parser,
        level: int = 1,
    ):
        """Create a level scene.

        Args:
            settings: Window, map, and timing settings.
            sprite_service: Service used to load and draw sprites.
            game_data: Validated game configuration.
            level: One-based level number.
        """
        self.settings = settings
        self.level = level
        self.sprite_service = sprite_service
        self.game_data = game_data
        self.freeze_condition: float | list[int] = 0
        self.frozen_at = time.time()

    def enter(self, engine: GameEngine) -> None:
        """Build the map, resources, entities, and systems for the level."""
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
            level=self.level,
            level_max_time=self.game_data.level_max_time,
            freeze=self.freeze,
            frozen=False,
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
        """Advance the level and return a replacement scene when needed."""
        self.resources.display_cheat = (
            pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL)
            or pr.is_key_down(pr.KeyboardKey.KEY_RIGHT_CONTROL)
        )

        if (
            pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE)
        ):
            from pacman.game.scenes.menu import MenuScene

            return MenuScene(self.settings, self.sprite_service)

        if self.resources.frozen:
            if isinstance(self.freeze_condition, list):
                should_unfreeze = any(
                    pr.is_key_pressed(key) for key in self.freeze_condition
                )
            else:
                should_unfreeze = (
                    time.time() - self.frozen_at >= self.freeze_condition
                )

            if should_unfreeze:
                self.resources.frozen = False
                self.freeze_callback()
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
            self.freeze([pr.KeyboardKey.KEY_SPACE], lambda: None)

        try:
            event = cast(
                GameOverEvent,
                next(
                    filter(
                        lambda e: isinstance(e, GameOverEvent),
                        engine.events.events,
                    )
                ),
            )
            from pacman.game.scenes.menu import MenuScene

            return GameOverScene(
                self.settings,
                event.score,
                MenuScene(self.settings, self.sprite_service),
                self.sprite_service,
            )

        except StopIteration:
            engine.events.drain()

        if self.resources.pacgum_count == 0:
            if self.resources.level == 10:
                from pacman.game.scenes.menu import MenuScene

                return WinScene(
                    self.settings,
                    self.resources.score,
                    MenuScene(self.settings, self.sprite_service),
                    self.sprite_service,
                )
            return GameScene(
                self.settings,
                self.sprite_service,
                self.game_data,
                level=self.resources.level + 1,
            )
        return None

    def render(self, engine: GameEngine) -> None:
        """Run all registered systems for the current frame."""
        for system in engine.systems:
            system.run()

    def exit(self, engine: GameEngine) -> None:
        """Clear the engine state when leaving the level."""
        engine.clear()

    def freeze(
        self,
        freeze_condition: float | list[int],
        callback: Callable[[], None],
    ) -> None:
        """Freeze level updates until a key is pressed or time elapses.

        Args:
            freeze_condition: Duration in seconds, or keys that unfreeze the
                level when pressed.
            callback: Function called when the freeze ends.
        """
        self.resources.frozen = True
        self.freeze_condition = freeze_condition
        self.frozen_at = time.time()
        self.freeze_callback = callback
