from pacman.game.settings import GameSettings
import pyray as pr

from pacman.engine.engine import GameEngine
from pacman.game.game import PacmanGame
from pacman.game.scenes.menu import MenuScene

pr.set_trace_log_level(pr.LOG_NONE)


def main():
    settings = GameSettings.from_window(
        window_width=1350,
        window_height=800,
    )

    scene = MenuScene(settings)
    with GameEngine(MenuScene(settings)) as engine:
        game = PacmanGame(engine, settings)
        game.make_full_setup()
        game.start_game()


if __name__ == "__main__":
    main()
