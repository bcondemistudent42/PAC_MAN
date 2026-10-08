from ...components.defaults.direction import Dir, Direction
from ...components.defaults.intention import Intention
from ...components.defaults.position import Position
from ...components.defaults.sprites import Sprites
from ...components.defaults.velocity import Velocity
from ...resources import Resources
from ..system import System


class MovementSystem(System):
    def __init__(self, resources: Resources):
        super().__init__([Position, Velocity, Direction, Intention])
        self.resources = resources
        self.direction_map = {
            Dir.LEFT: (-1, 0),
            Dir.RIGHT: (1, 0),
            Dir.UP: (0, -1),
            Dir.DOWN: (0, 1),
        }
        if resources.navigation_service is None:
            raise RuntimeError(
                "Navigation service is unavailable. Initialize game services "
                "before creating MovementSystem."
            )
        self.navigation = resources.navigation_service

    def run(self):
        if self.resources.frozen:
            return

        scale = self.resources.scale

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

            if (
                (is_aligned_x and is_aligned_y)
                or (
                    intention.direction == Dir.LEFT
                    and direction.direction == Dir.RIGHT
                )
                or (
                    intention.direction == Dir.RIGHT
                    and direction.direction == Dir.LEFT
                )
                or (
                    intention.direction == Dir.UP
                    and direction.direction == Dir.DOWN
                )
                or (
                    intention.direction == Dir.DOWN
                    and direction.direction == Dir.UP
                )
            ):
                position.x = target_x
                position.y = target_y

                intent_dx, intent_dy = self.direction_map[intention.direction]
                if self.navigation.is_walkable(cell_x + intent_dx, cell_y + intent_dy):
                    if direction.direction != intention.direction:
                        sprites = subscriber.get_component(Sprites)
                        sprites.sprite_index = 0

                    direction.direction = intention.direction

                curr_dx, curr_dy = self.direction_map[direction.direction]
                if not self.navigation.is_walkable(
                    cell_x + curr_dx, cell_y + curr_dy
                ):
                    continue

            dx, dy = self.direction_map[direction.direction]
            position.x += dx * velo.speed
            position.y += dy * velo.speed
