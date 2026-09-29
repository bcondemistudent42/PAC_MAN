from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.scared import Scared
from pacman.engine.components.defaults.target import Target
from pacman.engine.components.entity import Entity
from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources


class TargetSystem(System):
    def __init__(self, ressources: Ressources):
        super().__init__([Target, Position, Intention, Direction])
        self.ressources = ressources
        import time
        self.start = time.time()

    def run(self):
        # to delete later
        for each_subscriber in self.subscribers:
            behavior = each_subscriber.get_component(Target).behavior

            import time
            end = time.time()
            # to replace with component scared check if present for entity
            # and then check, do it also for the sprites stuff
            print(self.start - end)
            if self.start - end < -10:
                each_subscriber.get_component(Scared).scared = True
            if each_subscriber.get_component(Scared).scared:
                road = behavior.scared_behavior()
            else:
                road = behavior.find_pacman()
            self.change_direction(
                each_subscriber,
                road,
                behavior.ghost_coord
            )

    def change_direction(
        self,
        entity: Entity,
        right_way: list | None,
        ghost_coord: tuple[int, int]
    ):
        if not right_way:
            return

        x, y = ghost_coord
        x_way, y_way = right_way[-1]
        x_diff = x - x_way
        y_diff = y - y_way
        if x_diff == -1:
            entity.get_component(Intention).direction = Dir.RIGHT
        if x_diff == 1:
            entity.get_component(Intention).direction = Dir.LEFT
        if y_diff == -1:
            entity.get_component(Intention).direction = Dir.DOWN
        if y_diff == 1:
            entity.get_component(Intention).direction = Dir.UP

# TODO bug identified, when ghost in mid of two cases,
# it's not going anymore in the if diff 
# because it's one case ahead