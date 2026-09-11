from pacman.engine.components.component import Component

class Velocity(Component):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y