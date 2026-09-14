from dataclasses import dataclass
import heapq as hp


@dataclass
class Node:
    parent: tuple(int, int) | None | str
    heuristic : int | None
    cost : int | None
    total_cost_est : int | None
    coord: tuple(int, int)

    def __lt__(self, other: Node):
        return self.total_cost_est < other.total_cost_est

from abc import ABC, abstractmethod

class Behavior(ABC):
    def __init__(
        self,
        ghost_coord: tuple(int, int),
        pacman_coord: tuple(int, int),
        maze_size: tuple(int, int),
        maze: list[list[int]]
    ):
        self.ghost_coord = ghost_coord
        self.pacman_coord = pacman_coord
        self.maze_size = maze_size
        self.maze = maze

    @abstractmethod
    def find_pacman(self):
        pass

class BlinkyBehavior(Behavior):
    def __init__(
        self,
        ghost_coord: tuple[int, int],
        pacman_coord: tuple[int, int],
        maze_size: tuple[int, int],
        maze: list[list[int]]
    ):
        super().__init__(ghost_coord, pacman_coord, maze_size, maze)

    @staticmethod
    def heuristic(start: (int, int), end: (int, int)):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def find_pacman(self):

        visited = set()
        not_visited = []
        hp.heapify(not_visited)

        blinky_red = Node(
                    None,
                    self.heuristic(self.ghost_coord, self.pacman_coord),
                    0,
                    self.heuristic(self.ghost_coord, self.pacman_coord),
                    self.ghost_coord
        )

        hp.heappush(not_visited, blinky_red)

        maxtrix_height = len(matrix)
        matrix_width = len(matrix[0])
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
                (maxtrix_height, matrix_width)
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

    def output_north(self, actual_node: Node, goal: Node):
        x, y = actual_node.coord
        y -= 1
        estimated = self.heuristic((x, y), goal) + actual_node.cost + 1
        to_push = Node(
            (actual_node, actual_node.coord),
            self.heuristic((x, y), goal),
            actual_node.cost + 1,
            estimated,
            (x, y)
        )
        return to_push

    def output_south(self, actual_node: Node, goal: Node):
        x, y = actual_node.coord
        y += 1
        estimated = self.heuristic((x, y), goal) + actual_node.cost + 1
        to_push = Node(
            (actual_node, actual_node.coord),
            self.heuristic((x, y), goal),
            actual_node.cost + 1,
            estimated,
            (x, y)
        )
        return to_push

    def output_west(self, actual_node: Node, goal: Node):
        x, y = actual_node.coord
        x -= 1
        estimated = self.heuristic((x, y), goal) + actual_node.cost + 1
        to_push = Node(
            (actual_node, actual_node.coord),
            self.heuristic((x, y), goal),
            actual_node.cost + 1,
            estimated,
            (x, y)
        )
        return to_push

    def output_east(self, actual_node: Node, goal: Node):
        x, y = actual_node.coord
        x += 1
        estimated = self.heuristic((x, y), goal) + actual_node.cost + 1
        to_push = Node(
            (actual_node, actual_node.coord),
            self.heuristic((x, y), goal),
            actual_node.cost + 1,
            estimated,
            (x, y)
        )
        return to_push


    def add_neighbours(
        self,
        queu: hp.heapq,
        actual_node: Node,
        goal: (int, int),
        visited: list(Node),
        matrix_size: (int, int)
    ):

        which_node = ["N", "S", "W", "E"]

        actual_x, actual_y = actual_node.coord

        if actual_x == 0:
            which_node.remove("N")
        if actual_x == matrix_size[0] - 1:
            which_node.remove("S")
        if actual_y == 0:
            which_node.remove("W")
        if actual_y == matrix_size[1] - 1:
            which_node.remove("E")

        for cardinal in which_node:
            if cardinal == "N":
                check = self.output_north(actual_node, goal)
                if not check.coord in visited:
                    hp.heappush(queu, check)
            elif cardinal == "S":
                check = self.output_south(actual_node, goal)
                if not check.coord in visited:
                    hp.heappush(queu, check)
            elif cardinal == "W":
                check = self.output_west(actual_node, goal)
                if not check.coord in visited:
                    hp.heappush(queu, check)
            elif cardinal == "E":
                check = self.output_east(actual_node, goal)
                if not check.coord in visited:
                    hp.heappush(queu, check)

# to refacto pathfinding to adapt for maze of amazeing


# To create behavior component for each ghosts
matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

ghost = (0, 0)
pac_man = (14, 14)
m_size = (15, 15)

blinky = BlinkyBehavior(
    ghost,
    pac_man,
    m_size,
    matrix
)
road = blinky.find_pacman()
print(road)


