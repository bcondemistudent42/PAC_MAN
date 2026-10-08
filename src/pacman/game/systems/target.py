import time
from enum import Enum
from random import randint

from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.components.entity import Entity
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.components.respawn import Respawn
from pacman.game.components.scared import Scared
from pacman.game.components.target import Target
from pacman.game.resources import PacmanResources


class GhostState(Enum):
    CHASE = 1
    SCATTER = 2
    AFRAID = 3


class TargetSystem(System):
    def __init__(
        self,
        resources: PacmanResources,
        chase_duration: float = 20.0,
        scatter_duration: float = 7.0,
    ):
        super().__init__([Target, Position, Intention, Direction, Scared])
        if chase_duration <= 0 or scatter_duration <= 0:
            raise ValueError("Chase and scatter durations must be positive.")
        self.resources = resources
        self.behavior = GhostState.CHASE
        self.changed_behavior = time.time()
        self.chase_duration = chase_duration
        self.scatter_duration = scatter_duration
        self.paused_at: float | None = None

    def run(self):
        if self.resources.frozen:
            return

        now = time.time()
        scared_is_active = any(
            subscriber.get_component(Scared).scared
            or subscriber.get_component(Scared).end_scared
            for subscriber in self.subscribers
        )

        if scared_is_active:
            if self.paused_at is None:
                self.paused_at = now
        elif self.paused_at is not None:
            self.changed_behavior += now - self.paused_at
            self.paused_at = None

        current_duration = (
            self.chase_duration
            if self.behavior is GhostState.CHASE
            else self.scatter_duration
        )
        behavior_changed = (
            not scared_is_active
            and now - self.changed_behavior >= current_duration
        )
        if behavior_changed:
            self.behavior = (
                GhostState.SCATTER
                if self.behavior is GhostState.CHASE
                else GhostState.CHASE
            )
            self.changed_behavior = now

        if behavior_changed and not scared_is_active:
            for subscriber in self.subscribers:
                target = subscriber.get_component(Target)
                target.scatter_point = (
                    randint(0, target.maze_size[0] - 1),
                    randint(0, target.maze_size[1] - 1),
                )

        for each_subscriber in self.subscribers:
            actualy_scared = each_subscriber.get_component(Scared).scared
            actualy_ending_scared = each_subscriber.get_component(
                Scared
            ).end_scared
            actualy_dead = each_subscriber.get_component(Dead).dead

            ghost_state = (
                GhostState.AFRAID
                if actualy_scared or actualy_dead or actualy_ending_scared
                else self.behavior
            )
            target = each_subscriber.get_component(Target)
            behavior = target.behavior
            if ghost_state is GhostState.SCATTER:
                road = behavior.find_scatter(target.scatter_point)
                if (
                    not scared_is_active
                    and behavior.ghost_coord == target.scatter_point
                ):
                    target.scatter_point = (
                        randint(0, target.maze_size[0] - 1),
                        randint(0, target.maze_size[1] - 1),
                    )
            else:
                road = behavior.find_pacman(ghost_state)
            self.change_direction(each_subscriber, road, behavior.ghost_coord)
            if behavior.ghost_coord == behavior.corner and actualy_dead and each_subscriber.get_component(Velocity).speed != 0:
                each_subscriber.get_component(Velocity).speed = 0
                each_subscriber.get_component(Dead).ready_respawn = True
                respawn_comp = each_subscriber.get_component(Respawn)
                each_subscriber.get_component(Position).x = respawn_comp.x
                each_subscriber.get_component(Position).y = respawn_comp.y


    def change_direction(
        self,
        entity: Entity,
        right_way: list | None,
        ghost_coord: tuple[int, int],
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
