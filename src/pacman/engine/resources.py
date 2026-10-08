from dataclasses import dataclass
from typing import Callable

from .events.queue import EventsQueue
from .services.navigation import NavigationService
from .services.sprites import SpriteService


@dataclass
class Resources:
    freeze: Callable[[float, Callable], None]
    frozen: bool
    events: EventsQueue
    sprite_service: SpriteService
    navigation_service: NavigationService
    scale: float
    level_max_time: float
