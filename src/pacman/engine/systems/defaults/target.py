from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.target import Target
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources


class TargetSystem(System):
    def __init__(self, ressources: Ressources):
        super().__init__([Position, Velocity, Target])
        self.ressources = ressources
        self.first_run = True

    def run(self):
        # to name better the var to see later first make it work
        if self.first_run:
            for each_subscriber in self.subscribers:
                behavior_component = each_subscriber.get_component(Target)
                cell_size = each_subscriber.get_component(Target).cell_size


                x, y = self.pixel_to_matrix(
                    (each_subscriber.get_component(Position).x,
                    each_subscriber.get_component(Position).y),
                    cell_size
                )

                trg = each_subscriber.get_component(Target).target_coord
                x_target, y_target = self.pixel_to_matrix(
                    (trg.get_component(Position).x,
                    trg.get_component(Position).y),
                    cell_size
                )

                astar = behavior_component.behavior(
                    (x, y),
                    (x_target, y_target),
                    behavior_component.maze_size,
                    behavior_component.maze,
                )

                road = astar.find_pacman()
                print(road)
                # to see latee how to do compatible


    def pixel_to_matrix(self, coord: tuple[int, int], cell_size: int):
        x, y = coord
        return (int(x // cell_size), int(y // cell_size))