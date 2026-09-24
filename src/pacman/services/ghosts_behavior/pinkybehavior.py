
from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.position import Position
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

        pacman_direction = self.pacman.get_component(Direction).direction
        preshot_dist = 4

        x, y = self.pacman_coord

        print("BEFORE")
        print(x, y)
        # to handle out of the maze case
        if pacman_direction == Dir.UP:
            x -= preshot_dist
        elif pacman_direction == Dir.DOWN:
            x += preshot_dist
        elif pacman_direction == Dir.LEFT:
            y -= preshot_dist
        elif pacman_direction == Dir.RIGHT:
            y += preshot_dist

        if x < 0 or x >= self.maze_size[0] or y < 0 or y >= self.maze_size[1]:
            return
        print("AFTER\n")
        print(x, y)
        print()
        self.pacman_coord = (x, y)

    def find_pacman(self):
        solver = Astar(
            self.ghost_coord,
            self.pacman_coord,
            self.maze_size,
            self.maze
        )
        return solver.find_road()
