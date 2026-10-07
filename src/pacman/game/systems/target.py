import time

from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.components.entity import Entity
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.scared import Scared
from pacman.game.components.target import Target
from pacman.game.resources import resources


class TargetSystem(System):
    def __init__(self, resources: resources):
        super().__init__([Target, Position, Intention, Direction, Scared])
        self.resources = resources
        self.start = time.time()

    def run(self):
        for each_subscriber in self.subscribers:
            actualy_scared = each_subscriber.get_component(Scared).scared
            actualy_ending_scared = each_subscriber.get_component(Scared).end_scared
            actualy_dead = each_subscriber.get_component(Dead).dead
            check = False
            if actualy_scared or actualy_dead or actualy_ending_scared:
                check = True
            behavior = each_subscriber.get_component(Target).behavior
            road = behavior.find_pacman(check)
            self.change_direction(
                each_subscriber,
                road,
                behavior.ghost_coord
            )
            if behavior.ghost_coord == behavior.corner and actualy_dead:
                each_subscriber.get_component(Velocity).speed = 0
                each_subscriber.get_component(Dead).ready_respawn = True
                each_subscriber.get_component(Position).x = behavior.corner[0] * self.factory.get_formula()
                each_subscriber.get_component(Position).y = behavior.corner[1] * self.factory.get_formula()
                # to handle this case with bad coordinates
                # have to use matrix to pixel to find the function

    def change_direction(
        self,
        entity: Entity,
        right_way: list | None,
        ghost_coord: tuple[int, int]
    ):
        if not right_way:
            return

        x, y = ghost_coord
        x_way, y_way = right_way[-1]
        x_diff = x - x_way
        y_diff = y - y_way
        if x_diff == -1:
            entity.get_component(Intention).direction = Dir.RIGHT
        if x_diff == 1:
            entity.get_component(Intention).direction = Dir.LEFT
        if y_diff == -1:
            entity.get_component(Intention).direction = Dir.DOWN
        if y_diff == 1:
            entity.get_component(Intention).direction = Dir.UP