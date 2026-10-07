import pyray as pr

from pacman.engine.engine import GameEngine
from pacman.game.game import PacmanGame
from pacman.game.scenes.menu import MenuScene
from pacman.game.settings import GameSettings

pr.set_trace_log_level(pr.LOG_NONE)  # type: ignore


def main():
    settings = GameSettings.from_window(
        window_width=1440,
        window_height=1440,
    )

    scene = MenuScene(settings)
    pr.init_window(1440, 1440, "PACMAN")
    moni = pr.get_current_monitor()
    h = pr.get_monitor_height(moni)
    w = pr.get_monitor_width(moni)
    pr.set_window_position(w // 8, h // 8)
    pr.set_target_fps(60)

    with GameEngine(scene, 1440, 1440) as engine:
        game = PacmanGame(engine, settings)
        game.make_full_setup()
        scene.sprite_service = game.sprite_service
        game.start_game()


if __name__ == "__main__":
    main()
