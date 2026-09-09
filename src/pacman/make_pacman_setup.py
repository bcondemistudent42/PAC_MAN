import random

import mazegenerator as mg

from pacman.engine.ecs import Entity, Map, Position, Sprite, Velocity
from pacman.engine.game_engine import GameEngine
from pacman.engine.systems.systems import MovementSystem, SpriteSystem
from pacman.services.sprites import SpriteService, config


class PacmanSetup:

    def __init__(self, engine: GameEngine):
        self.engine = engine

    def make_full_setup(self):
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

        sprite_service = SpriteService("sprites/spritesheet.png", config)
        sprite_service.init_sprites()
        sprite_system = SpriteSystem({SpriteService: sprite_service})
        movement_system = MovementSystem(None)
        # to do properly somewhere else

        p = Position(10, 10)
        v = Velocity(2, 0)
        spr = Sprite("pacman-right-1")

        pac_man = Entity("pac_man")
        pac_man.add_component(p)
        pac_man.add_component(v)
        pac_man.add_component(spr)
        sprite_system.subscribe(pac_man)
        movement_system.subscribe(pac_man)

        self.engine.add_system(sprite_system)
        self.engine.add_system(movement_system)

        self.engine.add_entities(
            pac_man
        )

    # def create_ghosts_entity():
