from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.target import Target
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.systems.system import System


class TargetSystem(System):
    def __init__(self, ressources: dict):
        super().__init__([Position, Velocity, Target])
        self.first_run = True

    def run(self):
        # to name better the var to see later first make it work
        if self.first_run:
            for each_subscriber in self.subscribers:
                behavior_component = each_subscriber.get_component(Target)
                x = each_subscriber.get_component(Position).x
                y = each_subscriber.get_component(Position).y
                # ghosts_coord = (0, 0)
                pac_man_coord = (10, 10)
                astar = behavior_component.behavior(
                    (x, y),
                    pac_man_coord,
                    behavior_component.maze_size,
                    behavior_component.maze,
                )

                road = astar.find_pacman()
                print(road)
                # to see latee how to do compatible


def pixel_to_coord(display_maze_size: tuple[int, int], graph_size: tuple[int, int]):
    _x_diplay, _y_display = display_maze_size
    _x_graph, _y_graph = graph_size
