
from pacman.engine.components.component import Component


class Isdying(Component):
    def __init__(self) -> None:
        self.dying = False
