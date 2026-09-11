from pacman.engine.components.component import Component
import pyray as pr

class Color(Component):
    def __init__(self, color: pr.color):
        self.color = color
