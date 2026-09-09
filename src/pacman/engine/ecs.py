import pyray as pr
from typing import TypeVar, cast


class Component:
    pass


T = TypeVar("T", bound=Component)


class Entity:
    def __init__(self, id: str):
        self.id = id
        self.components: dict[type[Component], Component] = {}

    def add_component(self, component: Component):
        self.components[type(component)] = component

    def get_component(self, component: type[T]) -> T:
        return cast(T, self.components[component])

class Position(Component):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

class Velocity(Component):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Color(Component):
    def __init__(self, color: pr.color):
        self.color = color

class Size(Component):
    def __init__(self, size: int):
        self.size = size

# bcondemi feats

class Sprite(Component):
    def __init__(self, sprite_name: str):
        self.sprite_name = sprite_name

class Collision(Component):
    def __init__(self, tag: str):
        self.tag = tag

class Hitbox(Component):
    def __init__(
        self,
        width: int,
        height: int
    ):
        self.width = width
        self.height = height

class Map(Component):
    def __init__(self, map: list[list[int]]):
        self.map = map