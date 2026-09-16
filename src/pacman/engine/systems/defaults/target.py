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

                trg = each_subscriber.get_component(Target).target_coord
                x_target = trg.get_component(Position).x
                y_target = trg.get_component(Position).y
                print(x_target, y_target)
                # each_subscriber.get_component(Target)

                # ghosts_coord = (0, 0)
                astar = behavior_component.behavior(
                    (x // 30, y // 30),
                    (x_target // 30, y_target // 30),
                    behavior_component.maze_size,
                    behavior_component.maze,
                )

                    # 30 is because it's actually to set with ressources
                    # map_width = 10
                    # map_height = 10
                    # cell_width_px =30
                    # cell_height_px = 30

                road = astar.find_pacman()
                print(road)
                # to see latee how to do compatible


# def pixel_to_coord(
#     display_maze_size: tuple[int, int],
#     graph_size: tuple[int, int],
#     coord: tuple[int, int]
# ):
#     # x_diplay, y_display = display_maze_size
#     # x_graph, y_graph = graph_size
#     cell_size_pix = 30
#     graph_size = 10

#     x, y = coord

#     corect_x = x / 30
#     corect_y = y / 30



