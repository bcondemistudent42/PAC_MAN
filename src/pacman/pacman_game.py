import random

import mazegenerator as mg

from pacman.engine.ecs import Collision, Entity, Hitbox, Map, Position, Sprites, Velocity, KeyHook
from pacman.engine.game_engine import GameEngine
from pacman.engine.systems.systems import CollisionSystem, MovementSystem, SpriteSystem, KeySystem
from pacman.services.sprites import SpriteService, config
import pyray as pr

collision_system = CollisionSystem(None)

class PacmanGame:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.system = {} #system name class: system instance

    def start_game(self):
        self.engine.run()

    def system_init(self):
        sprite_sheet = "sprites/spritesheet.png"
        sprite_service = SpriteService(sprite_sheet, config)
        sprite_service.init_sprites()
        movement_system = MovementSystem(None)
        #collision_system = CollisionSystem(None)
        sprite_system = SpriteSystem({SpriteService: sprite_service})
        keys_system = KeySystem(None)

        self.system[SpriteSystem] = sprite_system
        self.system[MovementSystem] = movement_system
        self.system[CollisionSystem] = collision_system
        self.system[KeySystem] = keys_system

        self.engine.add_system([movement_system, sprite_system, collision_system, keys_system])

    def make_full_setup(self):
        self.system_init()
        self.make_entities_lvl()
        self.create_movable_entities()

    def make_entities_lvl(self) -> None:

        self.engine.add_entities(
            self.create_level(True)
        )
        for i in range(10):
            self.engine.add_entities(
                self.create_level()
            )

    def create_level(self, first_level: bool= False):
        my_maze = mg.MazeGenerator()
        if first_level:
            my_maze.generate(seed=42)
        else:
            my_maze.generate(seed=random.randint(0, 10000))

        level_entity = Entity("level_0")
        map_component = Map(my_maze.maze)
        level_entity.add_component(map_component)
        return level_entity

    def create_movable_entities(self):
        self.create_pacman()
        # self.create_ghosts()

    def create_pacman(self):

        # to spawn at the center of the map
        p = Position(150, 100)
        v = Velocity(1, 0)
        spr = Sprites(["pacman-right-1", "pacman-right-2", "pacman-right-3"])
        hitbox = Hitbox(10, 10)
        col = Collision("pacman")

        def on_left_key() -> None:
            print("Left key pressed")
            v.x = -5
            v.y = 0

        def on_right_key() -> None:
            print("Right key pressed")
            v.x = 5
            v.y = 0

        def on_up_key() -> None:
            print("Top key pressed")
            v.y = -5
            v.x = 0

        def on_down_key() -> None:
            print("Bot key pressed")
            v.y = 5
            v.x = 0

        keys = KeyHook(keys={
            pr.KEY_LEFT: on_left_key,
            pr.KEY_RIGHT: on_right_key,
            pr.KEY_UP: on_up_key,
            pr.KEY_DOWN: on_down_key,
        })


        pac_man = Entity("pac_man")
        pac_man.add_component(p)
        pac_man.add_component(v)
        pac_man.add_component(spr)
        pac_man.add_component(hitbox)
        pac_man.add_component(col)
        pac_man.add_component(keys)


        self.engine.add_entities(pac_man)

    def create_ghosts(self):
        self.create_inky()
        self.create_clyde()
        self.create_blinky()
        self.create_pinky()


    def create_inky(self):

        # to spaw at the left top corner
        p = Position(10, 180)
        v = Velocity(1, 0)
        spr = Sprites(["inky-right-1"])
        hitbox = Hitbox(10, 10)
        col = Collision("ghost")


        inky = Entity("inky")
        inky.add_component(p)
        inky.add_component(v)
        inky.add_component(spr)
        inky.add_component(hitbox)
        inky.add_component(col)

        self.engine.add_entities(inky)

    def create_clyde(self):

        # to spawn at the bottom right corner
        p = Position(190, 190)
        v = Velocity(1, 0)
        spr = Sprites(["clyde-right-1"])

        clyde = Entity("clyde")
        clyde.add_component(p)
        clyde.add_component(v)
        clyde.add_component(spr)

        self.engine.add_entities(clyde)

    def create_blinky(self):

        # to spawn at the bottom left corner
        p = Position(10, 190)
        v = Velocity(1, 0)
        spr = Sprites(["blinky-right-1"])

        blinky = Entity("blinky")
        blinky.add_component(p)
        blinky.add_component(v)
        blinky.add_component(spr)

        self.engine.add_entities(blinky)

    def create_pinky(self):

        # to spaw at the bottom left corner
        p = Position(190, 150)
        v = Velocity(1, 0)
        spr = Sprites(["pinky-right-1"])

        pinky = Entity("pinky")
        pinky.add_component(p)
        pinky.add_component(v)
        pinky.add_component(spr)

        self.engine.add_entities(pinky)

    @collision_system.router("pacman", "ghost")
    def handle_pacman_ghost_collision(
        first: Entity,
        second: Entity
    ) -> None:
        print("Collision entre Pacman et un Ghost")
