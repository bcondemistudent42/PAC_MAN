

from pacman.engine.components.component import Component
from pacman.engine.components.defaults.position import Position


class GhostScore(Component):
    def __init__(self, text: str, pos: Position, display: bool) -> None:
        self.text = text
        self.position = pos
        self.display = display
