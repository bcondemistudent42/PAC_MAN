from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.defaults.target import Target
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.components.entity import Entity
from pacman.engine.engine import GameEngine


class GhostFactory:
    def __init__(
        self, scale: float, maze: list[list[int]], pacman: Entity, engine: GameEngine
    ) -> None:
        self.SCALE = scale
        self.maze = maze
        self.pacman = pacman
        self.engine = engine

    def create(self, name: str) -> Entity:
        ghost = Entity(name)

        if name == "blinky":
            spr = Sprites(["blinky-right-1"], 0.1)
            t = Target((14, 18), self.pacman, (10, 10), self.maze)
            p = Position(14, 14)
            v = Velocity(0)
            col = Collision("ghost", {})
            hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)

            ghost.add_component(spr)
            ghost.add_component(p)
            ghost.add_component(t)
            ghost.add_component(v)
            ghost.add_component(col)
            ghost.add_component(hitbox)

        elif name == "inky":
            p = Position(10, 180)
            v = Velocity(3)
            spr = Sprites(["inky-right-1"], 0.1)
            hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)
            col = Collision("ghost", {})

            ghost.add_component(p)
            ghost.add_component(col)
            ghost.add_component(spr)
            ghost.add_component(v)
            ghost.add_component(hitbox)

        elif name == "clyde":
            p = Position(590, 590)
            spr = Sprites(["clyde-right-1"], 0.1)
            hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)
            col = Collision("ghost", {})

            ghost.add_component(p)
            ghost.add_component(col)
            ghost.add_component(spr)
            ghost.add_component(hitbox)

        elif name == "pinky":
            p = Position(290, 1050)
            col = Collision("ghost", {})
            hitbox = Hitbox(13 * self.SCALE, 13 * self.SCALE)
            spr = Sprites(["pinky-right-1"], 0.1)

            ghost.add_component(p)
            ghost.add_component(col)
            ghost.add_component(hitbox)
            ghost.add_component(spr)

        self.engine.add_entities(ghost)
        return ghost
