from pacman.engine.components.component import Component

class Display(Component):
    def __init__(self, flag: bool = True):
        self.flag = flag