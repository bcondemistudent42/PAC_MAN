from pacman.engine.components.component import Component


class Map(Component):
    def __init__(self, map: list[list[int]]):
        self.map = map
