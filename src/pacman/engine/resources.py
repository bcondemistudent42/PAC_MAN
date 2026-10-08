from abc import ABC, abstractmethod

from pacman.engine.events.queue import EventsQueue
from pacman.engine.services.navigation import NavigationService
from pacman.game.services.sprites import SpriteService
from dataclasses import dataclass


@dataclass
class Resources(ABC):
    sprite_service: SpriteService
    navigation_service: NavigationService
    events: EventsQueue
