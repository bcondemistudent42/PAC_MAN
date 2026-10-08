from dataclasses import dataclass

from .events.queue import EventsQueue
from .services.navigation import NavigationService
from .services.sprites import SpriteService


@dataclass
class Resources:
    events: EventsQueue
    sprite_service: SpriteService
    navigation_service: NavigationService
    scale: float
    level_max_time: float
