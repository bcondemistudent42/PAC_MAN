import pyray as pr

from pacman.game.scenes.endgame import EndGameScene


class GameOverScene(EndGameScene):
    """Display the game-over screen."""

    TITLE = "GAME OVER"
    TITLE_COLOR = pr.RED