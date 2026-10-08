from dataclasses import dataclass

from .events.queue import EventsQueue
from .services.navigation import NavigationService
from .services.sprites import SpriteService


@dataclass
class Resources:
    events: EventsQueue
    sprite_service: SpriteService | None = None
    navigation_service: NavigationService | None = None
    scale: float = 1.0
    level_max_time: float | None = None
