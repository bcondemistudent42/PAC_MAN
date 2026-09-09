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
        self.create_pacman_entity()

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

    def create_pacman_entity(self):

        # to see if can do 
        # to do properly somewhere else

        p = Position(10, 10)
        v = Velocity(2, 0)
        spr = Sprite("pacman-right-1")

        pac_man = Entity("pac_man")
        pac_man.add_component(p)
        pac_man.add_component(v)
        pac_man.add_component(spr)

        self.system[SpriteSystem].subscribe(pac_man)
        self.system[MovementSystem].subscribe(pac_man)

        self.engine.add_entities(pac_man)

    # def create_ghosts_entity():
