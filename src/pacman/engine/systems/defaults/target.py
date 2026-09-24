from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.target import Target
from pacman.engine.components.entity import Entity
from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources


class TargetSystem(System):
    def __init__(self, ressources: Ressources):
        super().__init__([Target, Position, Intention, Direction])
        self.ressources = ressources
        self.first_run = True

    def run(self):
        # if self.first_run: instiance the comrpotement else just run it
        for each_subscriber in self.subscribers:
            behavior_component = each_subscriber.get_component(Target)
            pacman = each_subscriber.get_component(Target).target

            finder = behavior_component.behavior(
                each_subscriber,
                pacman,
                behavior_component.maze_size,
                behavior_component.maze,
            )
            road = finder.find_pacman()

            self.change_direction(
                each_subscriber,
                road,
                finder.ghost_coord
            )
            # to see latee how to do compatible

    def change_direction(
        self,
        entity: Entity,
        right_way: list | None,
        ghost_coord: tuple[int, int]
    ):
        # return #to handle properly
        if not right_way:
            return

        x, y = ghost_coord
        # print("Ghost", x, y)
        # print("Next Cell", right_way[-1])
        x_way, y_way = right_way[-1]
        x_diff = x - x_way
        y_diff = y - y_way
        if x_diff == -1:
            # print("RIGHT")
            entity.get_component(Direction).direction = Dir.RIGHT
        if x_diff == 1:
            # print("LEFT")
            entity.get_component(Direction).direction = Dir.LEFT
        if y_diff == -1:
            # print("DOWN")
            entity.get_component(Direction).direction = Dir.DOWN
        if y_diff == 1:
            # print("UP")
            entity.get_component(Direction).direction = Dir.UP
        # else:
            # print("Problems")


# bug idntified, when ghost in mid of two cases, it's not going anymore in the if diff 
# because it's one case ahead