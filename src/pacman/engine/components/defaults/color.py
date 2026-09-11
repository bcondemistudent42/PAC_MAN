import pyray as pr

from pacman.engine.components.component import Component


class Color(Component):
    def __init__(self, color: pr.color):
        self.color = color
