import pyray as pr


class Component:
    pass

class Entity:
    def __init__(self, id: str):
        self.id = id
        self.components: dict[type[Component], Component] = {}

    def add_component(self, component: Component):
        self.components[type(component)] = component

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
    def __init__(self, img_path: str):
        self.img = pr.load_texture(img_path)

        if self.img == 0:
            raise FileNotFoundError(
                f"Missing file: {img_path}"
            )

# class Colision(Component):
#     def __init__(self, is_colliding: bool):
#         self.is_colliding = is_colliding

class Map(Component):
    def __init__(self, map: list[list[int]]):
        self.map = map