from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pacman.engine.resources import Resources
from pacman.game.services.parser import Parser

if TYPE_CHECKING:
    from pacman.game.services.maps import PacmanCell


@dataclass
class PacmanResources(Resources):
    data_score: Parser
    pacgum_count: int = 0
    score: int = 0
    matrix: list[list[PacmanCell]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.level_max_time = self.data_score.level_max_time
