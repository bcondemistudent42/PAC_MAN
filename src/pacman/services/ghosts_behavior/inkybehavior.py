from pacman.engine.components.defaults.direction import Dir
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.entity import Entity
from pacman.services.ghosts_behavior.astar import Astar
from pacman.services.ghosts_behavior.behavior import Behavior


# when a lot of pacgum is eaten, passing a thresholds to add velocity to the ghost
class InkyBehavior(Behavior):
    def __init__(
        self,
        ghost: Entity,
        blinky: Entity,
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
        self.blinky = blinky

    def find_pacman(self) -> list | None:

        preshot_dist = 2
        pacman_intention = self.pacman.get_component(Intention).direction

        x_blinky = self.blinky.get_component(Position).x
        y_blinky = self.blinky.get_component(Position).y
        x_blinky_graph, y_blinky_graph = self.pixel_to_matrix(
            (x_blinky, y_blinky),
            self.cell_size
        )

        x_inky = self.ghost.get_component(Position).x
        y_inky = self.ghost.get_component(Position).y
        x_inky_graph, y_inky_graph = self.pixel_to_matrix(
            (x_inky, y_inky),
            self.cell_size
        )
        self.ghost_coord = (x_inky_graph, y_inky_graph)

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

        good_coord_target = (x, y)

        workout = ((good_coord_target[0] - x_blinky_graph) * 2,
                   (good_coord_target[1] - y_blinky_graph) * 2)
        final = (x_blinky_graph + workout[0], y_blinky_graph + workout[1])
        if final[0] < 0 or final[0] >= self.maze_size[0] or final[1] < 0 or final[1] >= self.maze_size[1]:
            final = (x_before, y_before)

        output = self.solver.find_road(
            (x_inky_graph, y_inky_graph),
            final
        )
        if output is None:
            return [(x_before, y_before)]

        return output