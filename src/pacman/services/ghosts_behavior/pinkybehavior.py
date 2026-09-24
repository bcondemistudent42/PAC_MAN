
from pacman.engine.components.defaults.direction import Dir
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.entity import Entity
from pacman.services.ghosts_behavior.astar import Astar
from pacman.services.ghosts_behavior.behavior import Behavior


class PinkyBehavior(Behavior):
    def __init__(
        self,
        ghost: Entity,
        pacman: Entity,
        maze_size: tuple[int, int],
        maze: list[list[int]],
    ) -> None:

        super().__init__(
            ghost,
            pacman,
            maze_size,
            maze
        )

    def find_pacman(self):

        preshot_dist = 4
        pacman_intention = self.pacman.get_component(Intention).direction

        x, y = self.pacman_coord

        if pacman_intention == Dir.UP:
            y -= preshot_dist
        elif pacman_intention == Dir.DOWN:
            y += preshot_dist
        elif pacman_intention == Dir.LEFT:
            x -= preshot_dist
        elif pacman_intention == Dir.RIGHT:
            x += preshot_dist

        if x < 0 or x >= self.maze_size[0] or y < 0 or y >= self.maze_size[1]:
            pass
        else:
            self.pacman_coord = (x, y)

        solver = Astar(
            self.ghost_coord,
            self.pacman_coord,
            self.maze_size,
            self.maze
        )
        return solver.find_road()
