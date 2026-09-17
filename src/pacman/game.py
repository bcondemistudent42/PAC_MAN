import random

import mazegenerator as mg
import pyray as pr

from pacman.death import DeathSprites
from pacman.engine.components import Entity
from pacman.engine.components.defaults import (
    Collision,
    Hitbox,
    KeyHook,
    Map,
    Position,
    Sprites,
    Target,
    Velocity,
)
from pacman.engine.systems.defaults import (
    CollisionSystem,
    KeySystem,
    MovementSystem,
    SpriteSystem,
    TargetSystem,
)
from pacman.services.maps import PacmanMap
from pacman.services.sprites import SpriteService, config
from src.pacman.engine.engine import GameEngine

collision_system = CollisionSystem(None)


class PacmanGame:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.system = {}  # system name class: system instance

        map_width = 30
        map_height = 30

        cell_width_px = 24
        cell_height_px = 24 # DO NOT TOUCH

        map_pixel_width = map_width * cell_width_px
        map_pixel_height = map_height * cell_height_px

        self.SCALE = min(
            engine.window_height / map_pixel_height,
            engine.window_width / map_pixel_width,
        )
        print(self.SCALE)

        self.map_service = PacmanMap(engine, self.SCALE, map_width, map_height)

    def start_game(self):
        self.engine.run()

    def system_init(self):
        sprite_sheet = "sprites/spritesheet.png"
        sprite_service = SpriteService(sprite_sheet, config)
        sprite_service.init_sprites()
        movement_system = MovementSystem({})
        collision_system = CollisionSystem({})
        sprite_system = SpriteSystem(
            {SpriteService: sprite_service, "scale": self.SCALE}
        )
        keys_system = KeySystem({})
        target_sys = TargetSystem({})

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

    def create_pacman(self):

        # to spawn at the center of the map
        p = Position(150, 100)
        v = Velocity(1 * self.SCALE, 0)
        spr = Sprites(["pacman-right-1", "pacman-right-2", "pacman-right-3"], 0.1)
        hitbox = Hitbox(int(13 * self.SCALE), int(13 * self.SCALE))

        def on_left_key() -> None:
            if v.x < 0 and v.y == 0:
                return

            v.x = -1.1 * self.SCALE
            v.y = 0

            spr.sprite_index = 0
            spr.sprites = ["pacman-left-1", "pacman-left-2", "pacman-left-3"]

        def on_right_key() -> None:
            if v.x > 0 and v.y == 0:
                return
            v.x = 1.1 * self.SCALE
            v.y = 0
            spr.sprite_index = 0
            spr.sprites = ["pacman-right-1", "pacman-right-2", "pacman-right-3"]

        def on_up_key() -> None:
            if v.y < 0 and v.x == 0:
                return

            v.y = -1.1 * self.SCALE
            v.x = 0

            spr.sprite_index = 0
            spr.sprites = ["pacman-top-1", "pacman-top-2", "pacman-top-3"]

        def on_down_key() -> None:
            if v.y > 0 and v.x == 0:
                return

            v.y = 1.1 * self.SCALE
            v.x = 0

            spr.sprite_index = 0
            spr.sprites = ["pacman-bottom-1", "pacman-bottom-2", "pacman-bottom-3"]

        def handle_pacman_ghost_collision() -> None:
            spr.sprites = DeathSprites().PACMAN
            v.x = 0
            v.y = 0

        def handle_pacman_wall_left_collision() -> None:
            if v.x < 0:
                v.x = 0
                v.y = 0

        def handle_pacman_wall_right_collision() -> None:
            if v.x > 0:
                v.x = 0
                v.y = 0

        def handle_pacman_wall_top_collision() -> None:
            if v.y < 0:
                v.x = 0
                v.y = 0

        def handle_pacman_wall_bottom_collision() -> None:
            if v.y > 0:
                v.x = 0
                v.y = 0

        col = Collision(
            "pacman",
            {
                "ghost": handle_pacman_ghost_collision,
                "wall-left": handle_pacman_wall_left_collision,
                "wall-right": handle_pacman_wall_right_collision,
                "wall-top": handle_pacman_wall_top_collision,
                "wall-bottom": handle_pacman_wall_bottom_collision,
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

        self.engine.add_entities(pac_man)
        return pac_man

    def create_ghosts(self, pac_man):
        self.create_inky()
        self.create_clyde()
        self.create_blinky(pac_man)
        self.create_pinky()

    def create_inky(self):

        # to spaw at the left top corner
        p = Position(10, 180)
        v = Velocity(3, 0)
        spr = Sprites(["inky-right-1"], 0.1)
        hitbox = Hitbox(int(13 * self.SCALE), int(13 * self.SCALE))
        col = Collision("ghost", {})

        inky = Entity("inky")
        inky.add_component(p)
        inky.add_component(col)
        inky.add_component(spr)
        inky.add_component(v)
        inky.add_component(hitbox)

        self.engine.add_entities(inky)

    def create_clyde(self):

        # to spawn at the bottom right corner
        p = Position(590, 590)
        # v = Velocity(1, 0)
        spr = Sprites(["clyde-right-1"], 0.1)
        hitbox = Hitbox(int(13 * self.SCALE), int(13 * self.SCALE))

        col = Collision("ghost", {})

        clyde = Entity("clyde")
        clyde.add_component(p)
        clyde.add_component(col)
        clyde.add_component(spr)
        clyde.add_component(hitbox)
        self.engine.add_entities(clyde)

    def create_blinky(self, pac_man):

        maze = self.map_service.map
        # to spawn at the bottom left corner
        t = Target((14, 18), pac_man, (10, 10), maze)

        p = Position(14, 18)
        v = Velocity(0, 0)
        col = Collision("ghost", {})
        spr = Sprites(["blinky-right-1"], 0.1)
        hitbox = Hitbox(int(13 * self.SCALE), int(13 * self.SCALE))

        blinky = Entity("blinky")
        blinky.add_component(p)
        blinky.add_component(t)
        blinky.add_component(v)
        blinky.add_component(col)
        blinky.add_component(spr)
        blinky.add_component(hitbox)

        self.engine.add_entities(blinky)

    def create_pinky(self):

        # to spaw at the bottom left corner
        p = Position(290, 1050)
        # v = Velocity(1, 0)
        col = Collision("ghost", {})
        hitbox = Hitbox(int(13 * self.SCALE), int(13 * self.SCALE))

        spr = Sprites(["pinky-right-1"], 0.1)

        pinky = Entity("pinky")
        pinky.add_component(p)
        pinky.add_component(col)
        pinky.add_component(hitbox)

        pinky.add_component(spr)

        self.engine.add_entities(pinky)
