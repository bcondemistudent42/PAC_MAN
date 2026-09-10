from abc import ABC, abstractmethod
import pyray as pr
import itertools
from collections.abc import Callable

from pacman.engine.ecs import (
    Collision,
    Component,
    Entity,
    Hitbox,
    Position,
    Velocity,
    Sprites,
    KeyHook
)
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
                if (f_col.tag, s_col.tag) in self.router_map:
                    self.router_map[(f_col.tag, s_col.tag)](first, second)
                elif (s_col.tag, f_col.tag) in self.router_map:
                    self.router_map[(s_col.tag, f_col.tag)](first, second)


class MovementSystem(System):
    def __init__(self, ressources: dict):
        super().__init__([Position, Velocity])
        self.ressources = ressources

    @staticmethod
    def add_movement(Position, Velocity):
        return (Position.x + Velocity.x, Position.y + Velocity.y)

    def run(self):
        for subscriber in self.subscribers:
            actu_position = subscriber.get_component(Position)
            velo = subscriber.get_component(Velocity)

            actu_position.x += velo.x
            actu_position.y += velo.y

            # if actu_position.x > 270:
            #     from pacman.death_entities import make_death, DeathSprites
            #     make_death(subscriber, DeathSprites.PACMAN.value)


class SpriteSystem(System):
    def __init__(self, ressources: dict):
        super().__init__([Position, Sprites])
        self.ressources = ressources
        self.sprite_service = self.ressources[SpriteService]

    def run(self):
        for each_subscribed in self.subscribers:
            sprite_component = each_subscribed.get_component(Sprites)
            position_component = each_subscribed.get_component(Position)

            sprite_component.frame += pr.get_frame_time()

            if sprite_component.frame >= sprite_component.cooldown:
                if (
                    sprite_component.sprite_index < 
                    len(sprite_component.sprites_animation) - 1
                ):
                    sprite_component.sprite_index += 1
                sprite_component.frame = 0

            index = sprite_component.sprite_index
            x = position_component.x
            y = position_component.y

            pr.draw_texture_ex(
                self.ressources[SpriteService].get_sprite(
                    sprite_component.sprites_animation[index]
                ),
                pr.Vector2(x, y),
                0.0,
                5.0,
                pr.WHITE
            )

class KeySystem(System):
    def __init__(self, ressources: dict | None):
        super().__init__([KeyHook])
        self.ressources = ressources

    def run(self) -> None:
        for subscriber in self.subscribers:
            key_hook = subscriber.get_component(KeyHook)

            for key, on_press in key_hook.keys.items():
                if pr.is_key_pressed(key):
                    on_press() 
