
from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.components.entity import Entity
from pacman.engine.engine import GameEngine
from pacman.game.components.dead import Dead
from pacman.game.components.respawn import Respawn
from pacman.game.components.scared import Scared
from pacman.game.components.target import Target
from pacman.game.services.ghosts_behavior.blinkybehavior import BlinkyBehavior
from pacman.game.services.ghosts_behavior.clydebehavior import ClydeBehavior
from pacman.game.services.ghosts_behavior.inkybehavior import InkyBehavior
from pacman.game.services.ghosts_behavior.pinkybehavior import PinkyBehavior
from pacman.game.settings import GameSettings


class GhostFactory:
    def __init__(
        self,
        settings: GameSettings,
        maze: list[list[int]],
        pacman: Entity,
        engine: GameEngine,
    ) -> None:
        self.settings = settings
        self.maze = maze
        self.maze_size = (settings.map_width, settings.map_height)
        self.pac_man = pacman
        self.engine = engine
        self.cell_size = settings.cell_width_px * settings.scale
        self.tile_size = settings.cell_width_px * settings.scale
        self.blinky: Entity | None = None
        self.scared_ghost_spr = [
            "blue-ghost-1",
            "blue-ghost-2",
            "white-ghost-1",
            "white-ghost-2",
        ]

    def create_all(self) -> list[Entity]:
        """Create all ghosts in the order required by their behaviors."""
        return [
            self.create("clyde"),
            self.create("blinky"),
            self.create("inky"),
            self.create("pinky"),
        ]

    def create(self, name: str) -> Entity:
        ghost_data = {
            "blinky": (
                (0, 0),
                "blinky",
                BlinkyBehavior,
            ),
            "inky": (
                (0, self.maze_size[1] - 1),
                "inky",
                InkyBehavior,
            ),
            "clyde": (
                (self.maze_size[0] - 1, self.maze_size[1] - 1),
                "clyde",
                ClydeBehavior,
            ),
            "pinky": (
                (self.maze_size[0] - 1, 0),
                "pinky",
                PinkyBehavior,
            ),
        }
        if name not in ghost_data:
            supported_ghosts = ", ".join(ghost_data)
            raise ValueError(
                f"Unknown ghost {name!r}. Supported ghosts: {supported_ghosts}."
            )
        if name == "inky" and self.blinky is None:
            raise RuntimeError("Cannot create Inky before Blinky.")

        (tile_x, tile_y), sprite_name, behavior_type = ghost_data[name]
        ghost = Entity(name)
        position = Position(
            tile_x * self.tile_size + 8 * self.settings.scale,
            tile_y * self.tile_size + 8 * self.settings.scale,
        )
        direction_sprites = {
            direction: [
                f"{sprite_name}-{suffix}-1",
                f"{sprite_name}-{suffix}-2",
            ]
            for direction, suffix in (
                (Dir.RIGHT, "right"),
                (Dir.LEFT, "left"),
                (Dir.UP, "top"),
                (Dir.DOWN, "bottom"),
            )
        }
        resp_x = tile_x * self.tile_size + 8 * self.settings.scale
        resp_y = tile_y * self.tile_size + 8 * self.settings.scale
        ghost.add_component(
            [
                Scared(self.scared_ghost_spr),
                position,
                Velocity(self.settings.scale),
                Direction(Dir.DOWN, direction_sprites),
                Intention(Dir.DOWN),
                Collision("ghost"),
                Sprites([f"{sprite_name}-right-1"], 0.1),
                Hitbox(
                    13 * self.settings.scale,
                    13 * self.settings.scale,
                ),
                Respawn(resp_x, resp_y, self.settings.scale),
            ]
        )

        if name == "inky":
            if self.blinky is not None:
                behavior = behavior_type(
                    ghost,
                    self.blinky,
                    self.pac_man,
                    self.cell_size,
                    self.maze_size,
                    self.maze,
                )
            else:
                raise RuntimeError("Cannot create Inky before Blinky.")
        else:
            behavior = behavior_type(
                ghost,
                self.pac_man,
                self.cell_size,
                self.maze_size,
                self.maze,
            )

        ghost.add_component(
            Target(self.pac_man, self.maze_size, self.maze, behavior)
        )
        ghost.add_component(
            Dead(
                {
                    Dir.LEFT: ["ghost-eyes-left"],
                    Dir.RIGHT: ["ghost-eyes-right"],
                    Dir.UP: ["ghost-eyes-top"],
                    Dir.DOWN: ["ghost-eyes-bottom"],
                }
            )
        )

        self.engine.add_entities(ghost)
        if name == "blinky":
            self.blinky = ghost
        return ghost

    def get_formula(self):
        return self.tile_size + 8 * self.settings.scale

    def get_scale(self):
            return self.settings.scale
