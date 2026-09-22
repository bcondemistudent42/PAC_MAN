import pyray as pr

from pacman.game.game import PacmanGame
from src.pacman.engine.engine import GameEngine

pr.set_trace_log_level(pr.LOG_NONE)


def main():
    with GameEngine() as engine:
        game = PacmanGame(engine)
        game.make_full_setup()
        game.start_game()


if __name__ == "__main__":
    main()
