from pacman.engine.components.defaults.position import Position
from pacman.engine.components.entity import Entity
from pacman.game.services.ghosts_behavior.behavior import Behavior
from pacman.game.systems.target import GhostState


class ClydeBehavior(Behavior):
    def __init__(
        self,
        ghost: Entity,
        pacman: Entity,
        cell_size: float,
        maze_size: tuple[int, int],
        maze: list[list[int]],
    ) -> None:

        super().__init__(
            ghost,
            pacman,
            cell_size,
            maze_size,
            maze,
            (maze_size[0] - 1, maze_size[1] - 1),
        )
        self.margin = int(maze_size[0] * 0.25)
        self.last_pacman_coord: tuple[int, int] | None = None

    def find_pacman(
        self, state: GhostState
    ) -> list[tuple[int, int]] | None:
        if state is GhostState.AFRAID:
            return self.scared_behavior()

        x_ghost = self.ghost.get_component(Position).x
        y_ghost = self.ghost.get_component(Position).y
        x_ghost_graph, y_ghost_graph = self.pixel_to_matrix(
            (x_ghost, y_ghost), self.cell_size
        )

        self.ghost_coord = (x_ghost_graph, y_ghost_graph)
        x_pacman = self.pacman.get_component(Position).x
        y_pacman = self.pacman.get_component(Position).y

        x_pacman_graph, y_pacman_graph = self.pixel_to_matrix(
            (x_pacman, y_pacman), self.cell_size
        )

        target = (x_pacman_graph, y_pacman_graph)
        if (
            abs(x_ghost_graph - x_pacman_graph)
            + abs(y_ghost_graph - y_pacman_graph)
            <= self.margin
        ):
            if self.last_pacman_coord == (target):
                target = (x_ghost_graph, y_ghost_graph)
            else:
                target = self.corner

        output = self.solver.find_road((x_ghost_graph, y_ghost_graph), target)
        self.last_pacman_coord = (x_pacman_graph, y_pacman_graph)

        return output
