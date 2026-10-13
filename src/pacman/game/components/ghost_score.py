from pacman.engine.components.component import Component
from pacman.engine.components.defaults.position import Position


class GhostScore(Component):
    """Store the score label displayed after eating a ghost."""

    def __init__(self, text: str, pos: Position, display: bool) -> None:
        """Create a ghost-score display component.

        Args:
            text: Score text to display.
            pos: Position at which to display the text.
            display: Whether the score is currently visible.
        """
        self.text = text
        self.position = pos
        self.display = display
