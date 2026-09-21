from pacman.engine.components.component import Component


class Velocity(Component):
    def __init__(self, speed: float):
        self.speed = speed
