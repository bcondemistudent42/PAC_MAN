from ..component import Component


class Velocity(Component):
    def __init__(self, speed: float):
        self.speed = speed
        self.base_speed = speed
