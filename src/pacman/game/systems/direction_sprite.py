from pacman.engine.components.defaults import Sprites
from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.systems import System
from pacman.game.components.dead import Dead
from pacman.game.components.scared import Scared
from pacman.game.resources import resources


class DirectionSpriteSystem(System):
    def __init__(self, ressource: resources) -> None:
        super().__init__([Sprites, Direction])

    def run(self) -> None:
        for sub in self.subscribers:
            if sub.check_component(Dead) and sub.get_component(Dead).dead:
                sub.get_component(Sprites).sprites = sub.get_component(Dead).sprites[
                    sub.get_component(Direction).direction
                ]
            elif sub.check_component(Scared) and sub.get_component(Scared).scared:
                sub.get_component(Sprites).sprites = sub.get_component(
                    Scared).sprites
            else:
                sub.get_component(Sprites).sprites = sub.get_component(Direction).sprite_map[
                    sub.get_component(Direction).direction
                ]
