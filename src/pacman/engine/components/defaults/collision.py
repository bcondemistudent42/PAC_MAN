from collections.abc import Callable

from pacman.engine.components.component import Component


class Collision(Component):
    def __init__(self, tag: str, collision_map: dict[str, Callable]):
        self.tag = tag
        self.collision_map = collision_map
