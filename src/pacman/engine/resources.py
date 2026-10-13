from collections.abc import Callable
from dataclasses import dataclass

import pyray as pr

from .events.queue import EventsQueue
from .services.navigation import NavigationService
from .services.sprites import SpriteService


@dataclass
class Resources:
    """Shared runtime services and state used by engine systems."""

    freeze: Callable[
        [float | list[pr.KeyboardKey], Callable[[], None]], None
    ]
    frozen: bool
    events: EventsQueue
    sprite_service: SpriteService
    navigation_service: NavigationService
    scale: float
    level_max_time: float
