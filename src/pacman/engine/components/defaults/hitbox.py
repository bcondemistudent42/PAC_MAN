from pacman.engine.components.component import Component


class Hitbox(Component):
    def __init__(
        self, width: float, height: float, padding_x: float = 0, padding_y: float = 0
    ):
        self.width = width
        self.height = height
        self.padding_x = padding_x
        self.padding_y = padding_y
