import random

import mazegenerator as mg

from pacman.engine.ecs import Entity, Map, Position, Sprite, Velocity
from pacman.engine.game_engine import GameEngine
from pacman.engine.systems.systems import MovementSystem, SpriteSystem
from pacman.services.sprites import SpriteService, config


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
        sprite_system = SpriteSystem({SpriteService: sprite_service})

        self.system[SpriteSystem] = sprite_system
        self.system[MovementSystem] = movement_system

        self.engine.add_system([movement_system, sprite_system])


    def make_full_setup(self):
        self.system_init()
        self.make_entities_lvl()

        # to regroup into big function create each entities
        self.create_pacman()
        self.create_inky()
        self.create_clyde()
        self.create_blinky()
        self.create_pinky()

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

    def create_pacman(self):

        # to spawn at the center of the map
        p = Position(100, 100)
        v = Velocity(1, 0)
        spr = Sprite("pacman-right-1")

        pac_man = Entity("pac_man")
        pac_man.add_component(p)
        pac_man.add_component(v)
        pac_man.add_component(spr)

        self.system[SpriteSystem].subscribe(pac_man)
        self.system[MovementSystem].subscribe(pac_man)

        self.engine.add_entities(pac_man)

    def create_inky(self):

        # to spaw at the left top corner
        p = Position(10, 10)
        v = Velocity(1, 0)
        spr = Sprite("inky-right-1")

        inky = Entity("inky")
        inky.add_component(p)
        inky.add_component(v)
        inky.add_component(spr)

        self.system[SpriteSystem].subscribe(inky)
        self.system[MovementSystem].subscribe(inky)

        self.engine.add_entities(inky)



    def create_clyde(self):

        # to spawn at the bottom right corner
        p = Position(190, 190)
        v = Velocity(1, 0)
        spr = Sprite("clyde-right-1")

        clyde = Entity("clyde")
        clyde.add_component(p)
        clyde.add_component(v)
        clyde.add_component(spr)

        self.system[SpriteSystem].subscribe(clyde)
        self.system[MovementSystem].subscribe(clyde)

        self.engine.add_entities(clyde)


    def create_blinky(self):

        # to spawn at the bottom left corner
        p = Position(10, 190)
        v = Velocity(1, 0)
        spr = Sprite("blinky-right-1")

        blinky = Entity("blinky")
        blinky.add_component(p)
        blinky.add_component(v)
        blinky.add_component(spr)

        self.system[SpriteSystem].subscribe(blinky)
        self.system[MovementSystem].subscribe(blinky)

        self.engine.add_entities(blinky)


    def create_pinky(self):

        # to spaw at the bottom left corner
        p = Position(190, 10)
        v = Velocity(1, 0)
        spr = Sprite("pinky-right-1")

        pinky = Entity("pinky")
        pinky.add_component(p)
        pinky.add_component(v)
        pinky.add_component(spr)

        self.system[SpriteSystem].subscribe(pinky)
        self.system[MovementSystem].subscribe(pinky)

        self.engine.add_entities(pinky)