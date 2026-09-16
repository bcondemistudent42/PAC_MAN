from pacman.engine.components.component import Component


class Hitbox(Component):
    def __init__(self, width: int, height: int, padding_x: int = 0, padding_y: int = 0):
        self.width = width
        self.height = height
        self.padding_x = padding_x
        self.padding_y = padding_y
        # TODO: change coordinates for float
