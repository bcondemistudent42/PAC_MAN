import random

import mazegenerator as mg
import pyray as pr

from factories.ghost import GhostFactory
from pacman.engine.components import Entity
from pacman.engine.components.defaults import (
    Collision,
    Hitbox,
    KeyHook,
    Map,
    Position,
    Sprites,
    Velocity,
)
from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.engine import GameEngine
from pacman.engine.systems.defaults import (
    CollisionSystem,
    KeySystem,
    MovementSystem,
    SpriteSystem,
    TargetSystem,
)
from pacman.services.death import DeathSprites
from pacman.services.maps import PacmanMap
from pacman.services.sprites import SpriteService, config
from ressources import Ressources
from settings import GameSettings


class PacmanGame:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.system = {}
        self.settings = GameSettings.from_window(
            window_width=engine.window_width,
            window_height=engine.window_height,
        )
        self.ressources = Ressources(scale=self.settings.scale)

        self.map_service = PacmanMap(
            self.engine,
            self.settings.scale,
            self.settings.map_width,
            self.settings.map_height,
        )

    def start_game(self):
        self.ressources.matrix = self.matrix
        self.ressources.pos_to_cell = self.get_maze_cell_by_position
        self.ressources.sprite_service = self.sprite_service
        self.ressources.scale = self.settings.scale

        self.engine.run()

    def system_init(self):
        sprite_sheet = "sprites/spritesheet.png"
        self.sprite_service = SpriteService(sprite_sheet, config)
        collision_system = CollisionSystem(self.ressources)
        movement_system = MovementSystem(self.ressources)
        sprite_system = SpriteSystem(self.ressources)
        keys_system = KeySystem(self.ressources)
        target_sys = TargetSystem(self.ressources)

        self.system[SpriteSystem] = sprite_system
        self.system[MovementSystem] = movement_system
        self.system[CollisionSystem] = collision_system
        self.system[KeySystem] = keys_system
        self.system[TargetSystem] = target_sys

        self.engine.add_system(
            [movement_system, sprite_system, collision_system, keys_system, target_sys]
        )

    def make_full_setup(self):
        self.system_init()
        self.make_entities_lvl()
        self.map_service.generate_map()
        self.matrix = self.map_service.get_map_matrix()
        self.create_movable_entities()

    def make_entities_lvl(self) -> None:

        self.engine.add_entities(self.create_level(True))
        for i in range(10):
            self.engine.add_entities(self.create_level())

    def create_level(self, first_level: bool = False):
        my_maze = mg.MazeGenerator()
        if first_level:
            my_maze.generate(seed=42)
        else:
            my_maze.generate(seed=random.randint(0, 10000))

        level_entity = Entity("level")
        map_component = Map(my_maze.maze)
        level_entity.add_component(map_component)
        return level_entity

    def create_movable_entities(self):
        pac_man = self.create_pacman()
        self.create_ghosts(pac_man)

    def get_maze_cell_by_position(self, position: Position) -> tuple[int, int]:
        tile_size = 8 * self.settings.scale
        return (round(position.x / tile_size), round(position.y / tile_size))

    def get_target_position(
        self, position: Position, direction: tuple[int, int]
    ) -> tuple[float, float]:
        cell_x, cell_y = self.get_maze_cell_by_position(position)
        center_x = round((cell_x - 1) / 3) * 3 + 1
        center_y = round((cell_y - 1) / 3) * 3 + 1
        tile_size = 8 * self.settings.scale
        return (
            (center_x + direction[0] * 3) * tile_size,
            (center_y + direction[1] * 3) * tile_size,
        )

    def create_pacman(self):
        center = (self.settings.map_width // 2) * 3 + 1
        tile_size = 8 * self.settings.scale
        p = Position(center * tile_size, center * tile_size)
        v = Velocity(1 * self.settings.scale)
        spr = Sprites(["pacman-right-1", "pacman-right-2", "pacman-right-3"], 0.1)
        hitbox = Hitbox(13 * self.settings.scale, 13 * self.settings.scale)
        direction = Direction(Dir.DOWN)
        intention = Intention(Dir.DOWN)

        def on_left_key() -> None:
            intention.direction = Dir.LEFT

            spr.sprite_index = 0
            spr.sprites = ["pacman-left-1", "pacman-left-2", "pacman-left-3"]

        def on_right_key() -> None:
            intention.direction = Dir.RIGHT

            spr.sprite_index = 0
            spr.sprites = ["pacman-right-1", "pacman-right-2", "pacman-right-3"]

        def on_up_key() -> None:
            intention.direction = Dir.UP

            spr.sprite_index = 0
            spr.sprites = ["pacman-top-1", "pacman-top-2", "pacman-top-3"]

        def on_down_key() -> None:
            intention.direction = Dir.DOWN

            spr.sprite_index = 0
            spr.sprites = ["pacman-bottom-1", "pacman-bottom-2", "pacman-bottom-3"]

        def handle_pacman_ghost_collision() -> None:
            spr.sprites = DeathSprites().PACMAN
            v.speed = 0

        col = Collision(
            "pacman",
            {
                "ghost": handle_pacman_ghost_collision,
            },
        )

        keys = KeyHook(
            keys={
                pr.KEY_LEFT: on_left_key,
                pr.KEY_RIGHT: on_right_key,
                pr.KEY_UP: on_up_key,
                pr.KEY_DOWN: on_down_key,
            }
        )

        pac_man = Entity("pac_man")
        pac_man.add_component(p)
        pac_man.add_component(v)
        pac_man.add_component(spr)
        pac_man.add_component(hitbox)
        pac_man.add_component(col)
        pac_man.add_component(keys)
        pac_man.add_component(direction)
        pac_man.add_component(intention)

        self.engine.add_entities(pac_man)
        return pac_man

    def create_ghosts(self, pacman) -> None:
        ghosts_factory = GhostFactory(
            scale=self.settings.scale,
            maze=self.map_service.map,
            pacman=pacman,
            engine=self.engine,
        )

        ghosts_factory.create("inky")
        ghosts_factory.create("blinky")
        ghosts_factory.create("clyde")
        ghosts_factory.create("pinky")
