from pacman.engine.components.component import Component


class Velocity(Component):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
