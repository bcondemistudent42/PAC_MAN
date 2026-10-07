import pyray as pr

from pacman.engine.engine import GameEngine
from pacman.game.game import PacmanGame
from pacman.game.scenes.menu import MenuScene
from pacman.game.settings import GameSettings

pr.set_trace_log_level(pr.LOG_NONE) #type: ignore


def main():
    settings = GameSettings.from_window(
        window_width=1350,
        window_height=800,
    )

    scene = MenuScene(settings)
    with GameEngine(scene, 1350, 800) as engine:
        game = PacmanGame(engine, settings)
        game.make_full_setup()
        scene.sprite_service = game.sprite_service
        game.start_game()


if __name__ == "__main__":
    main()
