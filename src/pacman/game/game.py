import pyray as pr

from pacman.engine.components import Entity
from pacman.engine.components.defaults import (
    Collision,
    Hitbox,
    KeyHook,
    Position,
    Sprites,
    Target,
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
)
from pacman.game.ressources import Ressources
from pacman.game.settings import GameSettings
from pacman.services.death import DeathSprites
from pacman.services.ghosts_behavior.blinkybehavior import BlinkyBehavior
from pacman.services.ghosts_behavior.clydebehavior import ClydeBehavior
from pacman.services.ghosts_behavior.inkybehavior import InkyBehavior
from pacman.services.ghosts_behavior.pinkybehavior import PinkyBehavior
from pacman.services.maps import PacmanMap
from pacman.services.sprites import SpriteService, config


class PacmanGame:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.system = {}  # system name class: system instance
        self.ressources = {}

        self.map_width = 15
        self.map_height = 15

        cell_width_px = 24
        cell_height_px = 24
        # must always be the same, easier for everything, astar problem after if changed

        map_pixel_width = self.map_width * cell_width_px
        map_pixel_height = self.map_height * cell_height_px

        self.SCALE = min(
            engine.window_height / map_pixel_height,
            engine.window_width / map_pixel_width,
        )

        self.cell_size = cell_height_px * self.SCALE

        self.system = {}
        self.settings = GameSettings.from_window(
            window_width=engine.window_width,
            window_height=engine.window_height,
        )
        self.ressources = Ressources(self.engine.events, scale=self.settings.scale)

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
        from pacman.engine.systems.defaults import TargetSystem

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
        self.map_service.generate_map()
        self.matrix = self.map_service.get_map_matrix()
        self.create_movable_entities()

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
        direction = Direction(Dir.RIGHT)
        intention = Intention(Dir.RIGHT)

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

    def create_ghosts(self, pac_man):
        self.create_clyde(pac_man)
        blinky = self.create_blinky(pac_man)
        self.create_inky(pac_man, blinky)
        self.create_pinky(pac_man)

    def create_inky(self, pac_man: Entity, blinky: Entity):

        maze = self.map_service.map
        maze_size = (self.map_width, self.map_height)

        p = Position(670, 39)
        v = Velocity(1 * self.settings.scale)
        col = Collision("ghost", {})
        spr = Sprites(["inky-right-1"], 0.1)
        hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)
        direction = Direction(Dir.DOWN)
        intention = Intention(Dir.DOWN)

        inky = Entity("inky")

        inky.add_component(p)
        inky.add_component(v)
        inky.add_component(col)
        inky.add_component(spr)
        inky.add_component(hitbox)
        inky.add_component(direction)
        inky.add_component(intention)

        behavior = InkyBehavior(
            inky,
            blinky,
            pac_man,
            self.cell_size,
            maze_size,
            maze
        )

        t = Target(pac_man, maze_size, maze, behavior)
        inky.add_component(t)

        self.engine.add_entities(inky)

    def create_clyde(self, pac_man: Entity):

        maze = self.map_service.map
        maze_size = (self.map_width, self.map_height)

        p = Position(352, 490)
        v = Velocity(1 * self.settings.scale)
        col = Collision("ghost", {})
        spr = Sprites(["clyde-right-1"], 0.1)
        hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)
        direction = Direction(Dir.DOWN)
        intention = Intention(Dir.DOWN)

        clyde = Entity("clyde")

        clyde.add_component(p)
        clyde.add_component(v)
        clyde.add_component(col)
        clyde.add_component(spr)
        clyde.add_component(hitbox)
        clyde.add_component(direction)
        clyde.add_component(intention)

        behavior = ClydeBehavior(
            clyde,
            pac_man,
            self.cell_size,
            maze_size,
            maze
        )

        t = Target(pac_man, maze_size, maze, behavior)
        clyde.add_component(t)

        self.engine.add_entities(clyde)

    def create_blinky(self, pac_man):

        maze = self.map_service.map
        maze_size = (self.map_width, self.map_height)

        p = Position(40, 32)
        v = Velocity(1 * self.settings.scale)
        col = Collision("ghost", {})
        spr = Sprites(["blinky-right-1"], 0.1)
        hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)
        direction = Direction(Dir.DOWN)
        intention = Intention(Dir.DOWN)

        blinky = Entity("blinky")

        blinky.add_component(p)
        blinky.add_component(v)
        blinky.add_component(col)
        blinky.add_component(spr)
        blinky.add_component(hitbox)
        blinky.add_component(direction)
        blinky.add_component(intention)

        behavior = BlinkyBehavior(
            blinky,
            pac_man,
            self.cell_size,
            maze_size,
            maze
        )

        t = Target(pac_man, maze_size, maze, behavior)
        blinky.add_component(t)

        self.engine.add_entities(blinky)
        return blinky

    def create_pinky(self, pac_man):

        maze = self.map_service.map
        maze_size = (self.map_width, self.map_height)

        p = Position(590, 590)
        v = Velocity(1 * self.settings.scale)
        col = Collision("ghost", {})
        spr = Sprites(["pinky-right-1"], 0.1)
        hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)
        direction = Direction(Dir.DOWN)
        intention = Intention(Dir.DOWN)

        pinky = Entity("pinky")

        pinky.add_component(p)
        pinky.add_component(v)
        pinky.add_component(col)
        pinky.add_component(spr)
        pinky.add_component(hitbox)
        pinky.add_component(direction)
        pinky.add_component(intention)

        behavior = PinkyBehavior(
            pinky,
            pac_man,
            self.cell_size,
            maze_size,
            maze
        )

        t = Target(pac_man, maze_size, maze, behavior)
        pinky.add_component(t)

        self.engine.add_entities(pinky)