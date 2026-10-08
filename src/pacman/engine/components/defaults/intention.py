from ..component import Component
from .direction import Dir


class Intention(Component):
    def __init__(self, direction: Dir) -> None:
        self.direction = direction
