from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.target import Target
from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources


class TargetSystem(System):
    def __init__(self, ressources: Ressources):
        super().__init__([Target, Position, Intention, Direction])
        self.ressources = ressources
        self.first_run = True

    def run(self):
        # if self.first_run:
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

            self.change_direction(
                each_subscriber,
                road,
                (x, y))
            # to see latee how to do compatible


    def pixel_to_matrix(self, coord: tuple[int, int], cell_size: int):
        x, y = coord
        return (int(x // cell_size), int(y // cell_size))

    def change_direction(self, entity: Entity, right_way: list[tuple[int, int]], ghost_coord: tuple[int, int]):
        if not right_way:
            return
            # raise ValueError("ERROR LEN IS EMPTY")
            # return #to handle properly

# bug idntified, when ghost in mid of two cases, it's not going anymore in the if diff 
# because it's one case ahead

        x, y = ghost_coord
        print("Ghost", x, y)
        print("Next Cell", right_way[-1])
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