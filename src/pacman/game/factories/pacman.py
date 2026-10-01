import pyray as pr

from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.keyhook import KeyHook
from pacman.engine.components.defaults.position import Position
from pacman.game.components.respawn import Respawn
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.components.entity import Entity
from pacman.engine.engine import GameEngine
from pacman.game.settings import GameSettings


class PacmanFactory:
    def __init__(self, settings: GameSettings, engine: GameEngine) -> None:
        self.settings = settings
        self.engine = engine

    def create(self) -> Entity:
        tile_size = 8 * self.settings.scale
        pacman = Entity("pac_man")
        # to adapt the correct respawn and position of pacman
        pacman.add_component(Respawn(16 * tile_size, 16 * tile_size, 1.1 * self.settings.scale))
        pacman.add_component(Position(16 * tile_size, 16 * tile_size))
        pacman.add_component(Velocity(1.1 * self.settings.scale))
        pacman.add_component(
            Sprites(
                ["pacman-right-1", "pacman-right-2", "pacman-right-3"],
                0.10,
            )
        )
        pacman.add_component(
            Hitbox(8 * self.settings.scale, 8 * self.settings.scale)
        )
        pacman.add_component(Collision("pacman"))
        pacman.add_component(
            KeyHook(
                keys={
                    pr.KeyboardKey(pr.KeyboardKey.KEY_LEFT): Dir.LEFT,
                    pr.KeyboardKey(pr.KeyboardKey.KEY_RIGHT): Dir.RIGHT,
                    pr.KeyboardKey(pr.KeyboardKey.KEY_UP): Dir.UP,
                    pr.KeyboardKey(pr.KeyboardKey.KEY_DOWN): Dir.DOWN,
                }
            )
        )
        pacman.add_component(
            Direction(
                Dir.RIGHT,
                {
                    Dir.RIGHT: [
                        "pacman-right-1",
                        "pacman-right-2",
                        "pacman-right-3",
                    ],
                    Dir.LEFT: [
                        "pacman-left-1",
                        "pacman-left-2",
                        "pacman-left-3",
                    ],
                    Dir.UP: [
                        "pacman-top-1",
                        "pacman-top-2",
                        "pacman-top-3",
                    ],
                    Dir.DOWN: [
                        "pacman-bottom-1",
                        "pacman-bottom-2",
                        "pacman-bottom-3",
                    ],
                },
            )
        )
        pacman.add_component(Intention(Dir.RIGHT))

        self.engine.add_entities(pacman)
        return pacman
