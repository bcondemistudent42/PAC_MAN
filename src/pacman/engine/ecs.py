from typing import TypeVar, cast, Callable

import pyray as pr

from pacman.engine.components import (
    Collision,
    Color,
    Display,
    Hitbox,
    KeyHook,
    Map,
    Position,
    Size,
    Sprites,
    Velocity,
    Component,
)
from pacman.engine.components.entity import Entity
from pacman.engine.systems import (
    System,
    CollisionSystem,
    KeySystem,
    MovementSystem,
    SpriteSystem,
)

__all__ = [
    "Collision",
    "Color",
    "Display",
    "Hitbox",
    "KeyHook",
    "Map",
    "Position",
    "Size",
    "Sprites",
    "Velocity",
    "Component",
    "Entity",
    "System",
    "CollisionSystem",
    "KeySystem",
    "MovementSystem",
    "SpriteSystem",
]

# class Sprite(Component):
#     def __init__(self, sprite_name: str):
#         self.sprite_name = sprite_name







