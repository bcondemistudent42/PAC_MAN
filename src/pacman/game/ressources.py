from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pacman.engine.events.queue import EventsQueue

if TYPE_CHECKING:
    from pacman.engine.components.defaults.position import Position
    from pacman.services.maps import PacmanCell
    from pacman.services.sprites import SpriteService


@dataclass
class Ressources:
    events: EventsQueue
    matrix: list[list[PacmanCell]] = field(default_factory=list)
    pos_to_cell: Callable[[Position], tuple[int, int]] | None = None
    sprite_service: SpriteService | None = None
    scale: float = 1.0
