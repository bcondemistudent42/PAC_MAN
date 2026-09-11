from abc import ABC, abstractmethod
import pyray as pr
import itertools
from collections.abc import Callable
from pacman.engine.ecs import Component, Entity
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

