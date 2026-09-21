from pacman.engine.components.defaults.direction import Dir, Direction
from pacman.engine.components.defaults.intention import Intention
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources
from pacman.services.maps import PacmanCell


class MovementSystem(System):
    def __init__(self, ressources: Ressources):
        super().__init__([Position, Velocity, Direction, Intention])
        self.ressources = ressources
        self.direction_map = {
            Dir.LEFT: (-1, 0),
            Dir.RIGHT: (1, 0),
            Dir.UP: (0, -1),
            Dir.DOWN: (0, 1),
        }

    def run(self):
        matrix = self.ressources.matrix
        scale = self.ressources.scale

        tile_size = 8 * scale

        for subscriber in self.subscribers:
            position = subscriber.get_component(Position)
            velo = subscriber.get_component(Velocity)
            direction = subscriber.get_component(Direction)
            intention = subscriber.get_component(Intention)

            cell_x = round(position.x / tile_size)
            cell_y = round(position.y / tile_size)

            target_x = cell_x * tile_size
            target_y = cell_y * tile_size

            dist_x = abs(position.x - target_x)
            dist_y = abs(position.y - target_y)

            is_aligned_x = dist_x <= (velo.speed / 2.0)
            is_aligned_y = dist_y <= (velo.speed / 2.0)

            if is_aligned_x and is_aligned_y:
                position.x = target_x
                position.y = target_y

                intent_dx, intent_dy = self.direction_map[intention.direction]
                if (
                    0 <= cell_y + intent_dy < len(matrix)
                    and 0 <= cell_x + intent_dx < len(matrix[0])
                    and matrix[cell_y + intent_dy][cell_x + intent_dx]
                    != PacmanCell.WALL
                ):
                    direction.direction = intention.direction

                curr_dx, curr_dy = self.direction_map[direction.direction]
                if (
                    0 <= cell_y + curr_dy < len(matrix)
                    and 0 <= cell_x + curr_dx < len(matrix[0])
                    and matrix[cell_y + curr_dy][cell_x + curr_dx] == PacmanCell.WALL
                ):
                    continue

            dx, dy = self.direction_map[direction.direction]
            position.x += dx * velo.speed
            position.y += dy * velo.speed
