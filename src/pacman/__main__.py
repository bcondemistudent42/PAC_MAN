import pyray as pr

from pacman.engine.engine import GameEngine
from pacman.engine.services.sprites import SpriteService
from pacman.game.factories.sprites import SpriteFactory
from pacman.game.scenes.menu import MenuScene
from pacman.game.services.parser import parse
from pacman.game.settings import GameSettings

pr.set_trace_log_level(pr.LOG_NONE)  # type: ignore


def main():
    settings = GameSettings.from_window(
        window_width=2440,
        window_height=1440,
    )
    game_data = parse()

    pr.init_window(settings.window_width, settings.window_height, "PACMAN")
    pr.set_target_fps(60)

    main_sprites, map_sprites = SpriteFactory().create()
    sprite_service = SpriteService("sprites/spritesheet.png", main_sprites)
    sprite_service.add_spritesheet("sprites/creeper.png", map_sprites)
    scene = MenuScene(settings, sprite_service, game_data)

    with GameEngine(
        scene,
        settings.window_width,
        settings.window_height
    ) as engine:
        try:
            engine.run()
        finally:
            sprite_service.exit_sprites()


if __name__ == "__main__":
    main()