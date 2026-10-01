from pacman.engine.components.component import Component


class Respawn(Component):
    """Takes x and y, the coordinates where the entity have to respawn"""
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
