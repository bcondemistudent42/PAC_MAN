from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pacman.engine.resources import Resources
from pacman.game.services.parser import Parser

if TYPE_CHECKING:
    from pacman.game.services.maps import PacmanCell


@dataclass
class PacmanResources(Resources):
    """Extend engine resources with Pac-Man game state."""

    data_score: Parser
    pacgum_count: int = 0
    score: int = 0
    time_left: float = 0.0
    level: int = 1
    matrix: list[list[PacmanCell]] = field(default_factory=list)
    display_cheat: bool = False
    cheat_scared: bool = False
    cheat_corner: bool = False

    def __post_init__(self) -> None:
        """Synchronize the engine time limit with parsed game data."""
        self.level_max_time = self.data_score.level_max_time
