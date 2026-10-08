from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pacman.engine.resources import Resources
from pacman.game.services.parser import Parser, parse

if TYPE_CHECKING:
    from pacman.game.services.maps import PacmanCell


@dataclass
class PacmanResources(Resources):
    score: int = 0
    matrix: list[list[PacmanCell]] = field(default_factory=list)
    data_score: Parser = field(default_factory=parse)

    def __post_init__(self) -> None:
        self.level_max_time = self.data_score.level_max_time
