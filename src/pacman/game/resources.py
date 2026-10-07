from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pacman.engine.events.queue import EventsQueue
from pacman.game.services.parser import Parser, parse

if TYPE_CHECKING:
    from pacman.engine.services.navigation import NavigationService
    from pacman.game.services.maps import PacmanCell
    from pacman.game.services.sprites import SpriteService


@dataclass
class resources:
    events: EventsQueue
    matrix: list[list[PacmanCell]] = field(default_factory=list)
    sprite_service: SpriteService | None = None
    navigation_service: NavigationService | None = None
    scale: float = 1.0
    data_score: Parser = field(default_factory=parse)
