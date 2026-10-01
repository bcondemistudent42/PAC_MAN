from pacman.engine.components.defaults.position import Position
from pacman.engine.components.entity import Entity
from pacman.engine.engine import GameEngine
from pacman.engine.systems.defaults import (
    CollisionSystem,
    KeySystem,
    MovementSystem,
    PacmanIntentionSystem,
    SpriteSystem,
)
from pacman.game.systems.death import DeathSystem
from pacman.game.systems.score import ScoreSystem
from pacman.game.factories.ghost import GhostFactory
from pacman.game.factories.pacman import PacmanFactory
from pacman.game.resources import resources
from pacman.game.settings import GameSettings
from pacman.game.services.maps import PacmanMap
from pacman.game.services.sprites import (
    SpriteService,
    config,
    config_spritesheet_2,
)
from pacman.engine.systems.defaults import TargetSystem



class PacmanGame:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.system = {}
        self.pacman: Entity | None = None
        self.settings = GameSettings.from_window(
            window_width=engine.window_width,
            window_height=engine.window_height,
        )
        self.resources = resources(
            self.engine.events,
            scale=self.settings.scale,
        )
        self.map_service = PacmanMap(
            self.engine,
            self.settings.scale,
            self.settings.map_width,
            self.settings.map_height,
        )

    def start_game(self):
        self.resources.matrix = self.matrix
        self.resources.pos_to_cell = self.get_maze_cell_by_position
        self.resources.sprite_service = self.sprite_service
        self.resources.scale = self.settings.scale
        self.engine.run()

    def system_init(self):
        sprite_sheet = "sprites/spritesheet.png"
        self.sprite_service = SpriteService(sprite_sheet, config)
        self.sprite_service.add_spritesheet(
            "sprites/creeper.png", config_spritesheet_2)
        collision_system = CollisionSystem(self.resources)
        movement_system = MovementSystem(self.resources)
        sprite_system = SpriteSystem(self.resources)
        keys_system = KeySystem(self.resources)
        pacman_intention_system = PacmanIntentionSystem(self.resources)
        target_sys = TargetSystem(self.resources)
        death_system = DeathSystem(self.resources)
        self.death_sys = death_system
        score_sys = ScoreSystem(self.resources)
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
                score_sys,
            ]
        )

    def make_full_setup(self):
        self.system_init()
        self.map_service.generate_map()
        self.matrix = self.map_service.get_map_matrix()
        ghosts = self.create_movable_entities()
        self.add_ghost_to_death(ghosts)

    def create_movable_entities(self) -> list[Entity]:
        self.pacman = PacmanFactory(self.settings, self.engine).create()
        return GhostFactory(
            settings=self.settings,
            maze=self.map_service.map,
            pacman=self.pacman,
            engine=self.engine,
        ).create_all()

    def get_maze_cell_by_position(self, position: Position) -> tuple[int, int]:
        tile_size = 8 * self.settings.scale
        return (round(position.x / tile_size), round(position.y / tile_size))

    def add_ghost_to_death(self, ghosts: list[Entity]) -> None:
        assert self.pacman is not None
        self.death_sys.entt_to_resp.extend(ghosts)
        self.death_sys.entt_to_resp.append(self.pacman)
