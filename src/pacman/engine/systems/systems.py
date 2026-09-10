from abc import ABC, abstractmethod

import pyray as pr

pr.set_trace_log_level(pr.LOG_NONE)
import itertools
from collections.abc import Callable

from pacman.engine.ecs import Collision, Component, Entity, Hitbox, Position, Velocity, Sprites
from pacman.services.sprites import SpriteService


class System(ABC):
    def __init__(self, components: list[type[Component]]):
        self.subscribers: list[Entity] = []
        self.required_components: list[type[Component]] = components

    def subscribe(self, entity: Entity):
        for component in self.required_components:
            if not component in entity.components:
                raise ValueError("A definir")

        self.subscribers.append(entity)

    @abstractmethod
    def run():
        ...


class CollisionSystem(System):
    def __init__(self, ressources: dict | None):
        super().__init__([Position, Collision])
        self.ressources = ressources
        self.router_map: dict[
            tuple[str, str], Callable[[Entity, Entity], None]
        ] = {}

    def router(self, first: str, second: str) -> Callable:
        def marker(
            func: Callable[[Entity, Entity], None]
        ) -> Callable[[Entity, Entity], None]:
            self.router_map[(first, second)] = func
            self.router_map[(second, first)] = func
            return func
        return marker

    def run(self) -> None:
        for first, second in itertools.combinations(self.subscribers, 2):
            f_pos = first.get_component(Position)
            s_pos = second.get_component(Position)
            f_hit = first.get_component(Hitbox)
            s_hit = second.get_component(Hitbox)
            f_col = first.get_component(Collision)
            s_col = second.get_component(Collision)

            #print(f"tag 1: {f_col.tag}, tag 2: {s_col.tag}")
            if s_col.tag == f_col.tag:
                continue

            if (
                f_pos.x + f_hit.width >= s_pos.x and
                f_pos.x <= s_pos.x + s_hit.width and
                f_pos.y + f_hit.height >= s_pos.y and
                f_pos.y <= s_pos.y + s_hit.height
            ):
                if (f_col.tag, s_col.tag) in self.router_map or (s_col.tag, f_col.tag) in self.router_map:
                    self.router_map[(f_col.tag, s_col.tag)](first, second)


class MovementSystem(System):
    def __init__(self, ressources: dict | None):
        super().__init__([Position, Velocity])
        self.ressources = ressources

    @staticmethod
    def add_movement(Position, Velocity):
        return (Position.x + Velocity.x, Position.y + Velocity.y)

    def run(self):
        for subscriber in self.subscribers:
            actu_position = subscriber.components[Position]
            velo = subscriber.components[Velocity]
    
            #print(f"Position actuelle {actu_position}")

            actu_position.x += velo.x
            actu_position.y += velo.y

            #print(f"Nouvelle position: {actu_position}") 


class SpriteSystem(System):
    def __init__(self, ressources: dict | None):
        super().__init__([Position, Sprites])
        self.ressources = ressources
        self.sprite_service = self.ressources[SpriteService]

    def run(self):
        for each_subscribed in self.subscribers:
            for each_sprite in each_subscribed.components[Sprites].sprites_animation:

                x = each_subscribed.components[Position].x
                y = each_subscribed.components[Position].y

                pr.draw_texture(
                    self.ressources[SpriteService].map[each_sprite],
                    x, y,
                    pr.WHITE)


# class ColisionSystem(System):
#     def __init__(self):
#         super().__init__([Position, Colision])