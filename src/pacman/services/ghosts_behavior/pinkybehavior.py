
from pacman.engine.components.defaults.direction import Dir
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.entity import Entity
from pacman.services.ghosts_behavior.astar import Astar
from pacman.services.ghosts_behavior.behavior import Behavior


class PinkyBehavior(Behavior):
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
            maze
        )

    def find_pacman(self):

        preshot_dist = 4
        pacman_intention = self.pacman.get_component(Intention).direction

        x_ghost = self.ghost.get_component(Position).x
        y_ghost = self.ghost.get_component(Position).y
        x_ghost_graph, y_ghost_graph = self.pixel_to_matrix(
            (x_ghost, y_ghost),
            self.cell_size
        )

        self.ghost_coord = (x_ghost_graph, y_ghost_graph)
        x_pacman = self.pacman.get_component(Position).x
        y_pacman = self.pacman.get_component(Position).y

        x, y = self.pixel_to_matrix(
            (x_pacman, y_pacman),
            self.cell_size)

        x_before, y_before = x, y

        if pacman_intention == Dir.UP:
            y -= preshot_dist
        elif pacman_intention == Dir.DOWN:
            y += preshot_dist
        elif pacman_intention == Dir.LEFT:
            x -= preshot_dist
        elif pacman_intention == Dir.RIGHT:
            x += preshot_dist

        if x < 0 or x >= self.maze_size[0] or y < 0 or y >= self.maze_size[1]:
            good_coord_target = (x_before, y_before)
        else:
            good_coord_target = (x, y)

        solver = Astar(
            (x_ghost_graph, y_ghost_graph),
            good_coord_target,
            self.maze_size,
            self.maze
        )
        return solver.find_road()
