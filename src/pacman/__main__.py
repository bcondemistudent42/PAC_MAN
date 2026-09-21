import pyray as pr

from src.pacman.engine.engine import GameEngine
from src.pacman.game import PacmanGame

pr.set_trace_log_level(pr.LOG_NONE)


def main():
    with GameEngine() as engine:
        game = PacmanGame(engine)
        game.make_full_setup()
        game.start_game()


if __name__ == "__main__":
    # try:
    main()
# except Exception as e:
# print(f"\n[ERROR]: {e}\n")


# feat docs chore fix refactor
# to scale all the images
