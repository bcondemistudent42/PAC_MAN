from abc import ABC, abstractmethod

import pyray as pr

pr.set_trace_log_level(pr.LOG_NONE)
from pacman.engine.ecs import Component, Entity, Position, Sprite, Velocity


class System(ABC):
    def __init__(self, components: list[type[Component]]):
        self.subscribers: list[Entity] = []
        self.required_components: list[type[Component]] = []

    def subscribe(self, entity: Entity):
        for component in self.required_components:
            if not component in entity.components:
                raise ValueError("A definir")

        self.subscribers.append(entity)

    @abstractmethod
    def run():
        ...

class MovementSystem(System):
    def __init__(self):
        super().__init__([Position, Velocity])

    @staticmethod
    def add_movement(Position, Velocity):
        return (Position.x + Velocity.x, Position.y + Velocity.y)

    def run(self):
        for subscriber in self.subscribers:
            actu_position = subscriber.components[Position]
            velo = subscriber.components[Velocity]
    
            print(f"Position actuelle {actu_position}")

            actu_position.x += velo.x
            actu_position.y += velo.y

            print(f"Nouvelle position: {actu_position}") 


class SpriteSystem(System):
    def __init__(self):
        super().__init__([Position, Sprite])

    def run(self):
        for each_subscribed in self.subscribers:
            img = each_subscribed.components[Sprite].img
            print(img)

            x = each_subscribed.components[Position].x
            y = each_subscribed.components[Position].y

            pr.draw_texture(img, x, y, pr.WHITE)


# class ColisionSystem(System):
#     def __init__(self):
#         super().__init__([Position, Colision])