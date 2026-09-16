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
                pac_man_coord = (10, 10)
                self.behavior = (
                    (x, y),
                    pac_man_coord,
                    behavior_component.maze_size,
                    behavior_component.maze,
                )
                # road = self.behavior.find_pacman()
                # print(road)to see latee how to do compatible
