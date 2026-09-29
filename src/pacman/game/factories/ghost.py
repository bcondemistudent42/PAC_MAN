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
        self.cell_size = map_size[0] * self.SCALE
        self.tile_size = 8 * self.SCALE * 3

        self.scared_ghost_spr = [
            "blue-ghost-1",
            "blue-ghost-2",
            "white-ghost-1",
            "white-ghost-2"
        ]

    def create(self, name: str) -> Entity:
        ghost = Entity(name)

        # to handle the +8 and all hardcoded value
        if name == "blinky":

            self.blinky = ghost
            position = Position(
                14 * self.tile_size + 8 * self.SCALE, 1 * self.tile_size + 8 * self.SCALE
            )

            scared = Scared(self.scared_ghost_spr)
            velocity = Velocity(1 * self.SCALE)
            collision = Collision("ghost", {})
            sprite = Sprites(["blinky-right-1"], 0.1)
            hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)

            direction_sprites_map = {
                Dir.RIGHT: ["blinky-right-1", "blinky-right-2"],
                Dir.LEFT: ["blinky-left-1", "blinky-left-2"],
                Dir.UP: ["blinky-top-1", "blinky-top-2"],
                Dir.DOWN: ["blinky-bottom-1", "blinky-bottom-2"],
            }

            intention = Intention(Dir.DOWN)
            direction = Direction(Dir.DOWN, direction_sprites_map)

            ghost.add_component(
                [
                    scared,
                    position,
                    velocity,
                    direction,
                    intention,
                    collision,
                    sprite,
                    hitbox
                ]
            )

            behavior = BlinkyBehavior(
                ghost,
                self.pac_man,
                self.cell_size,
                self.maze_size,
                self.maze
            )

            target = Target(
                self.pac_man,
                self.maze_size,
                self.maze,
                behavior
            )
            ghost.add_component(target)

        elif name == "inky":
            scared = Scared(self.scared_ghost_spr)

            position = Position(
                1 * self.tile_size + 8 * self.SCALE, 14 * self.tile_size + 8 * self.SCALE
            )

            velocity = Velocity(1 * self.SCALE)
            collision = Collision("ghost", {})
            sprite = Sprites(["inky-right-1"], 0.1)
            hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)

            direction_sprites_map = {
                Dir.RIGHT: ["inky-right-1", "inky-right-2"],
                Dir.LEFT: ["inky-left-1", "inky-left-2"],
                Dir.UP: ["inky-top-1", "inky-top-2"],
                Dir.DOWN: ["inky-bottom-1", "inky-bottom-2"],
            }

            direction = Direction(Dir.DOWN, direction_sprites_map)
            intention = Intention(Dir.DOWN)

            ghost.add_component(
                        [
                            scared,
                            position,
                            velocity,
                            direction,
                            intention,
                            collision,
                            sprite,
                            hitbox
                        ]
                    )

            behavior = InkyBehavior(
                ghost,
                self.blinky,
                self.pac_man,
                self.cell_size,
                self.maze_size,
                self.maze
            )

            target = Target(self.pac_man, self.maze_size, self.maze, behavior)
            ghost.add_component(target)

        elif name == "clyde":
            scared = Scared(self.scared_ghost_spr)

            position = Position(
                1 * self.tile_size + 8 * self.SCALE, 1 * self.tile_size + 8 * self.SCALE
            )
            # to see the *1

            velocity = Velocity(1 * self.SCALE)
            collision = Collision("ghost", {})
            sprite = Sprites(["clyde-right-1"], 0.1)
            hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)

            direction_sprites_map = {
                Dir.RIGHT: ["clyde-right-1", "clyde-right-2"],
                Dir.LEFT: ["clyde-left-1", "clyde-left-2"],
                Dir.UP: ["clyde-top-1", "clyde-top-2"],
                Dir.DOWN: ["clyde-bottom-1", "clyde-bottom-2"],
            }

            direction = Direction(Dir.DOWN, direction_sprites_map)
            intention = Intention(Dir.DOWN)

            ghost.add_component(
                    [
                        scared,
                        position,
                        velocity,
                        direction,
                        intention,
                        collision,
                        sprite,
                        hitbox
                    ]
                )

            behavior = ClydeBehavior(
                ghost,
                self.pac_man,
                self.cell_size,
                self.maze_size,
                self.maze
            )

            target = Target(self.pac_man, self.maze_size, self.maze, behavior)
            ghost.add_component(target)

        elif name == "pinky":
            scared = Scared(self.scared_ghost_spr)

            position = Position(
                (self.maze_size[0] - 1) * self.tile_size + 8 * self.SCALE,
                (self.maze_size[0] - 1)* self.tile_size + 8 * self.SCALE
            )

            velocity = Velocity(1 * self.SCALE)
            collision = Collision("ghost", {})
            sprite = Sprites(["pinky-right-1"], 0.1)
            hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)

            direction_sprites_map = {
                Dir.RIGHT: ["pinky-right-1", "pinky-right-2"],
                Dir.LEFT: ["pinky-left-1", "pinky-left-2"],
                Dir.UP: ["pinky-top-1", "pinky-top-2"],
                Dir.DOWN: ["pinky-bottom-1", "pinky-bottom-2"],
            }

            intention = Intention(Dir.DOWN)
            direction = Direction(Dir.DOWN, direction_sprites_map)

            ghost.add_component(
                [
                    scared,
                    position,
                    velocity,
                    direction,
                    intention,
                    collision,
                    sprite,
                    hitbox
                ]
            )

            behavior = PinkyBehavior(
                ghost,
                self.pac_man,
                self.cell_size,
                self.maze_size,
                self.maze
            )

            target   = Target(self.pac_man, self.maze_size, self.maze, behavior)
            ghost.add_component(target)

        self.engine.add_entities(ghost)
        return ghost
