import heapq as hp
from dataclasses import dataclass


@dataclass
class Node:
    """Represent one candidate node in an A* search."""

    parent: tuple["Node", tuple[int, int]] | None
    heuristic: int
    cost: int
    total_cost_est: int
    coord: tuple[int, int]

    def __lt__(self, other: Node) -> bool:
        """Compare nodes by their estimated total path cost."""
        if not self.total_cost_est or not other.total_cost_est:
            return False
        return self.total_cost_est < other.total_cost_est


class Astar:
    """Find routes through a maze using the A* search algorithm."""

    def __init__(
        self,
        maze_size: tuple[int, int],
        maze: list[list[int]],
    ) -> None:
        """Create a solver for a maze.

        Args:
            maze_size: Maze dimensions as ``(width, height)``.
            maze: Maze wall representation.
        """
        self.maze_size = maze_size
        self.maze = maze

    @staticmethod
    def heuristic(start: tuple[int, int], end: tuple[int, int]) -> int:
        """Return the Manhattan distance between two coordinates."""
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    # to pass ghost cord and pacman cord directly in parameter
    # rename them into ghost and target instead, clearer
    # readapt the other behavior to be clean

    def find_road(
        self,
        ghost_coord: tuple[int, int],
        pacman_coord: tuple[int, int],
    ) -> list[tuple[int, int]] | None:
        """Find a route from a ghost coordinate to a target coordinate.

        Args:
            ghost_coord: Starting maze coordinate.
            pacman_coord: Destination maze coordinate.

        Returns:
            Coordinates to follow, or ``None`` when no route exists.
        """

        visited: set[tuple[int, int]] = set()
        not_visited: list[Node] = []
        hp.heapify(not_visited)

        start_node = Node(
            None,
            self.heuristic(ghost_coord, pacman_coord),
            0,
            self.heuristic(ghost_coord, pacman_coord),
            ghost_coord,
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
                pacman_coord,
                visited,
                (maxtrix_height, matrix_width),
            )
            if actual_node.coord == pacman_coord:
                return self.get_way(actual_node)
        return None

    def get_way(self, actual_node: Node) -> list[tuple[int, int]]:
        """Reconstruct the route ending at a search node."""
        output: list[tuple[int, int]] = []
        node_path: tuple[Node, tuple[int, int]] = (
            actual_node,
            actual_node.coord,
        )
        while node_path[0].parent:
            output.append(node_path[1])
            node_path = node_path[0].parent
        return output

    def add_neighbours(
        self,
        queu: list[Node],
        actual_node: Node,
        goal: tuple[int, int],
        visited: set[tuple[int, int]],
        matrix_size: tuple[int, int],
    ) -> None:
        """Add walkable neighboring nodes to the search queue.

        Args:
            queu: Priority queue of pending nodes.
            actual_node: Node whose neighbors are being expanded.
            goal: Destination coordinate.
            visited: Coordinates already expanded.
            matrix_size: Search bounds as ``(width, height)``.
        """

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
                    self.heuristic((new_x, actual_y), goal)
                    + actual_node.cost
                    + 1,
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
