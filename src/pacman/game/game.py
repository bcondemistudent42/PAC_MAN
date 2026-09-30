from pacman.engine.components.defaults.position import Position
from pacman.engine.engine import GameEngine
from pacman.engine.systems.defaults import (
    CollisionSystem,
    KeySystem,
    MovementSystem,
    PacmanIntentionSystem,
    SpriteSystem,
)
from pacman.engine.systems.defaults.death import DeathSystem
from pacman.engine.systems.defaults.score import ScoreSystem
from pacman.game.factories.ghost import GhostFactory
from pacman.game.factories.pacman import PacmanFactory
from pacman.game.ressources import Ressources
from pacman.game.settings import GameSettings
from pacman.services.maps import PacmanMap
from pacman.services.sprites import SpriteService, config, config_spritesheet_2


class PacmanGame:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.system = {}
        self.settings = GameSettings.from_window(
            window_width=engine.window_width,
            window_height=engine.window_height,
        )
        self.ressources = Ressources(
            self.engine.events, scale=self.settings.scale)
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
        self.sprite_service.add_spritesheet(
            "sprites/creeper.png", config_spritesheet_2)
        collision_system = CollisionSystem(self.ressources)
        movement_system = MovementSystem(self.ressources)
        sprite_system = SpriteSystem(self.ressources)
        keys_system = KeySystem(self.ressources)
        pacman_intention_system = PacmanIntentionSystem(self.ressources)
        target_sys = TargetSystem(self.ressources)
        death_system = DeathSystem(self.ressources)
        score_sys = ScoreSystem(self.ressources)
        self.system[SpriteSystem] = sprite_system
        self.system[MovementSystem] = movement_system
        self.system[CollisionSystem] = collision_system
        self.system[KeySystem] = keys_system
        self.system[PacmanIntentionSystem] = pacman_intention_system
        self.system[TargetSystem] = target_sys
        self.system[ScoreSystem] = score_sys

        self.engine.add_system(
            [
                keys_system,
                collision_system,
                movement_system,
                sprite_system,
                pacman_intention_system,
                target_sys,
                death_system,
                score_sys
            ]
        )

    def make_full_setup(self):
        self.system_init()
        self.map_service.generate_map()
        self.matrix = self.map_service.get_map_matrix()
        self.create_movable_entities()

    def create_movable_entities(self):
        pacman = PacmanFactory(self.settings.scale, self.engine).create()
        GhostFactory(
            scale=self.settings.scale,
            maze=self.map_service.map,
            pacman=pacman,
            engine=self.engine,
            maze_size=(self.settings.map_width, self.settings.map_height),
            map_size=(self.settings.cell_width_px,
                      self.settings.cell_height_px),
        ).create_all()

    def get_maze_cell_by_position(self, position: Position) -> tuple[int, int]:
        tile_size = 8 * self.settings.scale
        return (round(position.x / tile_size), round(position.y / tile_size))
