from dataclasses import dataclass
import heapq as hp

def output_north(goal: Node):
    x, y = actual_node.coord
    y -= 1
    estimated = heuristic((x, y), goal) + actual_node.cost + 1
    to_push = Node(
        (actual_node, actual_node.coord),
        heuristic((x, y), goal),
        actual_node.cost + 1,
        estimated,
        (x, y)
    )
    return to_push

def output_south(goal: Node):
    x, y = actual_node.coord
    y += 1
    estimated = heuristic((x, y), goal) + actual_node.cost + 1
    to_push = Node(
        (actual_node, actual_node.coord),
        heuristic((x, y), goal),
        actual_node.cost + 1,
        estimated,
        (x, y)
    )
    return to_push

def output_west(goal: Node):
    x, y = actual_node.coord
    x -= 1
    estimated = heuristic((x, y), goal) + actual_node.cost + 1
    to_push = Node(
        (actual_node, actual_node.coord),
        heuristic((x, y), goal),
        actual_node.cost + 1,
        estimated,
        (x, y)
    )
    return to_push

def output_east(goal: Node):
    x, y = actual_node.coord
    x += 1
    estimated = heuristic((x, y), goal) + actual_node.cost + 1
    to_push = Node(
        (actual_node, actual_node.coord),
        heuristic((x, y), goal),
        actual_node.cost + 1,
        estimated,
        (x, y)
    )
    return to_push


def add_neighbours(queu: hp.heapq, actual_node: Node, goal: (int, int), visited: list(Node), matrix_size: (int, int)):

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
            check = output_north(goal)
            if not check.coord in visited:
                hp.heappush(queu, check)
        elif cardinal == "S":
            check = output_south(goal)
            if not check.coord in visited:
                hp.heappush(queu, check)
        elif cardinal == "W":
            check = output_west(goal)
            if not check.coord in visited:
                hp.heappush(queu, check)
        elif cardinal == "E":
            check = output_east(goal)
            if not check.coord in visited:
                hp.heappush(queu, check)

def heuristic(start: (int, int), end: (int, int)):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# To create behavior component for each ghosts
matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

@dataclass
class Node:
    parent: tuple(int, int) | None | str
    heuristic : int | None
    cost : int | None
    total_cost_est : int | None
    coord: tuple(int, int)

    def __lt__(self, other: Node):
        return self.total_cost_est < other.total_cost_est

pac_man_coord = (7, 7)
visited = []
not_visited = []
hp.heapify(not_visited)
# hp.heappush(not_visited, 21)

# if pacman ate a lot of gum increase it's speed

ghost_coord = (0, 0)

blinky_red = Node(
            None,
            heuristic(ghost_coord, pac_man_coord),
            0,
            heuristic(ghost_coord, pac_man_coord),
            ghost_coord
)

hp.heappush(not_visited, blinky_red)

maxtrix_height = len(matrix)
matrix_width = len(matrix[0])
# to do a check a all the width is the same

while not_visited:

    actual_node = hp.heappop(not_visited)
    if actual_node.coord in visited:
        continue
    visited.append(actual_node.coord)


    add_neighbours(
        not_visited,
        actual_node,
        pac_man_coord,
        visited,
        (maxtrix_height, matrix_width)
    )
    if actual_node.coord == pac_man_coord:
        print("SUCCESSSFUL")
        print("==========")
        output = []

        actual_node = (actual_node, actual_node.coord)
        while actual_node[0].parent:
            output.append(actual_node[1])
            actual_node = actual_node[0].parent
        print(output)
        exit()
