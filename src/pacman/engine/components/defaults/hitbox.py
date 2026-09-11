from pacman.engine.components.component import Component


class Hitbox(Component):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
