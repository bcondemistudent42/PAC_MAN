import heapq as hp
from dataclasses import dataclass


@dataclass
class Node:
    parent: tuple[int, int] | None | str
    heuristic: int | None
    cost: int | None
    total_cost_est: int | None
    coord: tuple[int, int]

    def __lt__(self, other: Node):
        if not self.total_cost_est or not other.total_cost_est:
            return False
        return self.total_cost_est < other.total_cost_est



class Astar:
    def __init__(
        self,
        ghost_coord: tuple[int, int],
        pacman_coord: tuple[int, int],
        maze_size: tuple[int, int],
        maze: list[list[int]],
    ):
        self.ghost_coord = ghost_coord
        self.pacman_coord = pacman_coord
        self.maze_size = maze_size
        self.maze = maze


    @staticmethod
    def heuristic(start: tuple[int, int], end: tuple[int, int]):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def find_road(self) -> list | None:

        visited = set()
        not_visited = []
        hp.heapify(not_visited)

        start_node = Node(
            None,
            self.heuristic(self.ghost_coord, self.pacman_coord),
            0,
            self.heuristic(self.ghost_coord, self.pacman_coord),
            self.ghost_coord,
        )

        hp.heappush(not_visited, start_node)

        maxtrix_height = self.maze_size[0]
        matrix_width = self.maze_size[1]
        # to do a check a all the width is the same

        while not_visited:
            actual_node = hp.heappop(not_visited)
            if actual_node.coord in visited:
                continue
            visited.add(actual_node.coord)

            self.add_neighbours(
                not_visited,
                actual_node,
                self.pacman_coord,
                visited,
                (maxtrix_height, matrix_width),
            )
            if actual_node.coord == self.pacman_coord:
                return self.get_way(actual_node)

    def get_way(self, actual_node: Node):
        output = []
        actual_node = (actual_node, actual_node.coord)
        while actual_node[0].parent:
            output.append(actual_node[1])
            actual_node = actual_node[0].parent
        return output

    def add_neighbours(
        self,
        queu: hp.heapq,
        actual_node: Node,
        goal: (int, int),
        visited: set(int),
        matrix_size: (int, int),
    ):

        actual_x, actual_y = actual_node.coord

        if actual_y >= matrix_size[1] or actual_x >= matrix_size[0]:
            return

        if actual_y == 0 or (actual_x, actual_y - 1) in visited:
            pass
        else:
            if self.maze[actual_y][actual_x] & 1 == 0:
                to_push = Node(
                    (actual_node, actual_node.coord),
                    self.heuristic((actual_x, actual_y - 1), goal),
                    actual_node.cost + 1,
                    self.heuristic((actual_x, actual_y - 1), goal)
                    + actual_node.cost
                    + 1,
                    (actual_x, actual_y - 1),
                )
                hp.heappush(queu, to_push)
        if actual_y >= matrix_size[1] or (actual_x + 1, actual_y) in visited:
            pass
        else:
            # EST
            if self.maze[actual_y][actual_x] >> 1 & 1 == 0:
                new_x = actual_x + 1
                to_push = Node(
                    (actual_node, actual_node.coord),
                    self.heuristic((new_x, actual_y), goal),
                    actual_node.cost + 1,
                    self.heuristic((new_x, actual_y), goal) + actual_node.cost + 1,
                    (new_x, actual_y),
                )
                hp.heappush(queu, to_push)
        if actual_x >= matrix_size[0] or (actual_x, actual_y + 1) in visited:
            pass
        else:
            # SOUTH
            # print("SOUTH")
            if self.maze[actual_y][actual_x] >> 2 & 1 == 0:
                to_push = Node(
                    (actual_node, actual_node.coord),
                    self.heuristic((actual_x, actual_y + 1), goal),
                    actual_node.cost + 1,
                    self.heuristic((actual_x, actual_y + 1), goal)
                    + actual_node.cost
                    + 1,
                    (actual_x, actual_y + 1),
                )
                hp.heappush(queu, to_push)
        if actual_x == 0 or (actual_x - 1, actual_y) in visited:
            pass
        else:
            if self.maze[actual_y][actual_x] >> 3 & 1 == 0:
                to_push = Node(
                    (actual_node, actual_node.coord),
                    self.heuristic((actual_x - 1, actual_y), goal),
                    actual_node.cost + 1,
                    self.heuristic((actual_x - 1, actual_y), goal)
                    + actual_node.cost
                    + 1,
                    (actual_x - 1, actual_y),
                )
                hp.heappush(queu, to_push)