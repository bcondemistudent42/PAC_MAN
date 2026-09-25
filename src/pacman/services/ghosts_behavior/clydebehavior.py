from pacman.engine.components.defaults.position import Position
from pacman.engine.components.entity import Entity
from pacman.services.ghosts_behavior.astar import Astar
from pacman.services.ghosts_behavior.behavior import Behavior


# when a lot of pacgum is eaten, passing a thresholds to add velocity to the ghost
class ClydeBehavior(Behavior):
    def __init__(
        self,
        ghost: Entity,
        pacman: Entity,
        cell_size: float,
        maze_size: tuple[int, int],
        maze: list[list[int]],
    ):

        super().__init__(
            ghost,
            pacman,
            cell_size,
            maze_size,
            maze
        )

    def find_pacman(self) -> list | None:
        x_ghost = self.ghost.get_component(Position).x
        y_ghost = self.ghost.get_component(Position).y
        x_ghost_graph, y_ghost_graph = self.pixel_to_matrix(
            (x_ghost, y_ghost), self.cell_size
            )

        self.ghost_coord = (x_ghost_graph, y_ghost_graph)
        x_pacman = self.pacman.get_component(Position).x
        y_pacman = self.pacman.get_component(Position).y

        x_pacman_graph, y_pacman_graph = (self.pixel_to_matrix(
            (x_pacman, y_pacman),
            self.cell_size)
        )

        solver = Astar(
            (x_ghost_graph, y_ghost_graph),
            (x_pacman_graph, y_pacman_graph),
            self.maze_size,
            self.maze
        )
        return solver.find_road()