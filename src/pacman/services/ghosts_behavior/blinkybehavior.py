from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.target import Target
from pacman.engine.components.entity import Entity
from pacman.services.ghosts_behavior.astar import Astar
from pacman.services.ghosts_behavior.behavior import Behavior


# when a lot of pacgum is eaten, passing a thresholds to add velocity to the ghost
class BlinkyBehavior(Behavior):
    def __init__(
        self,
        ghost: Entity,
        pacman: Entity,
        maze_size: tuple[int, int],
        maze: list[list[int]],
    ):

        super().__init__(
            ghost,
            pacman,
            maze_size,
            maze
        )

    def find_pacman(self) -> list | None:
        solver = Astar(
            self.ghost_coord,
            self.pacman_coord,
            self.maze_size,
            self.maze
        )
        return solver.find_road()