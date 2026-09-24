from pacman.engine.components.entity import Entity
from pacman.services.ghosts_behavior.astar import Astar
from pacman.services.ghosts_behavior.behavior import Behavior


class InkyBehavior(Behavior):
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
        # to make the correct stuff, with vector workout
        return solver.find_road()