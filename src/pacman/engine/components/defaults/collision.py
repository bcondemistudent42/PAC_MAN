from pacman.engine.components.component import Component


class Collision(Component):
    def __init__(self, tag: str):
        self.tag = tag
