from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.scared import Scared
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.target import Target
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.components.entity import Entity
from pacman.engine.engine import GameEngine
from pacman.services.ghosts_behavior.blinkybehavior import BlinkyBehavior
from pacman.services.ghosts_behavior.clydebehavior import ClydeBehavior
from pacman.services.ghosts_behavior.inkybehavior import InkyBehavior
from pacman.services.ghosts_behavior.pinkybehavior import PinkyBehavior


class GhostFactory:
    def __init__(
        self,
        scale: float,
        maze: list[list[int]],
        pacman: Entity,
        engine: GameEngine,
        maze_size: tuple[int, int],
        map_size: tuple[int, int],
    ) -> None:
        self.SCALE = scale
        self.maze = maze
        self.maze_size = maze_size
        self.pac_man = pacman
        self.engine = engine
        self.cell_size = map_size[0] * scale
        self.tile_size = 24 * scale
        self.blinky: Entity | None = None
        self.scared_ghost_spr = [
            "blue-ghost-1",
            "blue-ghost-2",
            "white-ghost-1",
            "white-ghost-2",
        ]

    def create_all(self) -> None:
        """Create all ghosts in the order required by their behaviors."""
        self.create("clyde")
        self.create("blinky")
        self.create("inky")
        self.create("pinky")

    def create(self, name: str) -> Entity:
        ghost_data = {
            "blinky": (
                (self.maze_size[0] - 1, 1),
                "blinky",
                BlinkyBehavior,
            ),
            "inky": (
                (1, self.maze_size[1] - 1),
                "inky",
                InkyBehavior,
            ),
            "clyde": ((1, 1), "clyde", ClydeBehavior),
            "pinky": (
                (self.maze_size[0] - 1, self.maze_size[1] - 1),
                "pinky",
                PinkyBehavior,
            ),
        }
        if name not in ghost_data:
            raise ValueError(f"Unknown ghost: {name}")
        if name == "inky" and self.blinky is None:
            raise RuntimeError("Blinky must be created before Inky")

        (tile_x, tile_y), sprite_name, behavior_type = ghost_data[name]
        ghost = Entity(name)
        position = Position(
            tile_x * self.tile_size + 8 * self.SCALE,
            tile_y * self.tile_size + 8 * self.SCALE,
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
        ghost.add_component(
            [
                Scared(self.scared_ghost_spr),
                position,
                Velocity(self.SCALE),
                Direction(Dir.DOWN, direction_sprites),
                Intention(Dir.DOWN),
                Collision("ghost"),
                Sprites([f"{sprite_name}-right-1"], 0.1),
                Hitbox(13 * self.SCALE, 13 * self.SCALE),
            ]
        )

        if name == "inky":
            assert self.blinky is not None
            behavior = behavior_type(
                ghost,
                self.blinky,
                self.pac_man,
                self.cell_size,
                self.maze_size,
                self.maze,
            )
        else:
            behavior = behavior_type(
                ghost,
                self.pac_man,
                self.cell_size,
                self.maze_size,
                self.maze,
            )

        ghost.add_component(Target(self.pac_man, self.maze_size, self.maze, behavior))
        self.engine.add_entities(ghost)
        if name == "blinky":
            self.blinky = ghost
        return ghost
