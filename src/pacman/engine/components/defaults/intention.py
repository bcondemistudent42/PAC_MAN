from pacman.engine.components.component import Component
from pacman.engine.components.defaults.direction import Dir


class Intention(Component):
    def __init__(self, direction: Dir) -> None:
        self.direction = direction
