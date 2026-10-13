import pyray as pr

from pacman.game.scenes.endgame import EndGameScene


class WinScene(EndGameScene):
    """Display the completion screen using the game-over presentation."""

    TITLE = "CONGRATULATIONS"
    TITLE_COLOR = pr.BLUE
