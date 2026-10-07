import random
from enum import Enum

from mazegenerator import MazeGenerator

from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.entity import Entity
from pacman.engine.engine import GameEngine
from pacman.game.settings import GameSettings


class PacmanCell(Enum):
    EMPTY = 0
    WALL = 1
    PACGUM = 2


class PacmanMap:
    def __init__(self, engine: GameEngine, settings: GameSettings) -> None:
        self.generator = MazeGenerator(
            size=(settings.map_width, settings.map_height),
            perfect=True,
            seed=48515,
        )

        self.TILE_SIZE = 8 * settings.scale
        self.scale = settings.scale
        self.engine = engine
        self.map = []
        self.settings = settings

        self.sprite_matrix = []
        self.logic_matrix = []

    def break_dead_ends(self, maze: list[list[int]]) -> list[list[int]]:
        height = len(maze)
        if height == 0:
            return maze
        width = len(maze[0])

        def count_2x2_walls(r: int, c: int) -> int:
            count = 0
            if maze[r][c] & 2:
                count += 1
            if maze[r + 1][c] & 2:
                count += 1
            if maze[r][c] & 4:
                count += 1
            if maze[r][c + 1] & 4:
                count += 1
            return count

        def can_break_h(y: int, x: int, min_walls: int = 1) -> bool:
            if maze[y][x] == 15 or maze[y][x + 1] == 15:
                return False
            if not (maze[y][x] & 2):
                return False
            return not (
                (
                    y > 0
                    and x < width - 1
                    and count_2x2_walls(y - 1, x) <= min_walls
                )
                or (
                    y < height - 1
                    and x < width - 1
                    and count_2x2_walls(y, x) <= min_walls
                )
            )

        def can_break_v(y: int, x: int, min_walls: int = 1) -> bool:
            if maze[y][x] == 15 or maze[y + 1][x] == 15:
                return False
            if not (maze[y][x] & 4):
                return False
            return not (
                (
                    x > 0
                    and y < height - 1
                    and count_2x2_walls(y, x - 1) <= min_walls
                )
                or (
                    x < width - 1
                    and y < height - 1
                    and count_2x2_walls(y, x) <= min_walls
                )
            )

        lines = []
        for y in range(height):
            lines.append(("H", y))
        for x in range(width):
            lines.append(("V", x))

        for i in range(len(lines) - 1, 0, -1):
            j = random.randint(0, i)
            lines[i], lines[j] = lines[j], lines[i]

        for line_type, idx in lines:
            if line_type == "H":
                y = idx
                for x in range(width - 1):
                    if can_break_h(y, x, min_walls=2):
                        maze[y][x] &= ~2
                        maze[y][x + 1] &= ~8
            else:
                x = idx
                for y in range(height - 1):
                    if can_break_v(y, x, min_walls=2):
                        maze[y][x] &= ~4
                        maze[y + 1][x] &= ~1

        remaining_walls = []
        for y in range(height):
            for x in range(width - 1):
                if maze[y][x] & 2:
                    remaining_walls.append(("H", y, x))
        for y in range(height - 1):
            for x in range(width):
                if maze[y][x] & 4:
                    remaining_walls.append(("V", y, x))

        for i in range(len(remaining_walls) - 1, 0, -1):
            j = random.randint(0, i)
            remaining_walls[i], remaining_walls[j] = (
                remaining_walls[j],
                remaining_walls[i],
            )

        for wtype, y, x in remaining_walls:
            if random.random() < 0.30:
                if wtype == "H" and can_break_h(y, x, min_walls=1):
                    maze[y][x] &= ~2
                    maze[y][x + 1] &= ~8
                elif wtype == "V" and can_break_v(y, x, min_walls=1):
                    maze[y][x] &= ~4
                    maze[y + 1][x] &= ~1

        return maze

    def get_map_matrix(self) -> list[list[PacmanCell]]:
        """Retourne la matrice logique du niveau pour le système de mouvement."""
        return self.logic_matrix

    def maze_to_matrix(self) -> None:
        """Génère la matrice visuelle et la matrice logique dans l'instance."""
        self.sprite_matrix = [
            ["" for _ in range(len(self.map[0]) * 3)]
            for _ in range(len(self.map) * 3)
        ]

        for y, line in enumerate(self.map):
            for x, hexa_rep in enumerate(line):
                cell = hexa_rep

                nord = bool(cell & 1)
                est = bool(cell & (1 << 1))
                sud = bool(cell & (1 << 2))
                ouest = bool(cell & (1 << 3))

                if nord and est and sud and ouest:
                    self.sprite_matrix[y * 3][x * 3] = "creeper-1"
                    self.sprite_matrix[y * 3][x * 3 + 1] = "creeper-2"
                    self.sprite_matrix[y * 3][x * 3 + 2] = "creeper-3"
                    self.sprite_matrix[y * 3 + 1][x * 3] = "creeper-4"
                    self.sprite_matrix[y * 3 + 1][x * 3 + 1] = "creeper-5"
                    self.sprite_matrix[y * 3 + 1][x * 3 + 2] = "creeper-6"
                    self.sprite_matrix[y * 3 + 2][x * 3] = "creeper-7"
                    self.sprite_matrix[y * 3 + 2][x * 3 + 1] = "creeper-8"
                    self.sprite_matrix[y * 3 + 2][x * 3 + 2] = "creeper-9"

                    continue

                self.sprite_matrix[y * 3 + 1][x * 3 + 1] = ""  # Centre vide

                # Bords
                if nord:
                    self.sprite_matrix[y * 3][x * 3 + 1] = "wall-top"
                if est:
                    self.sprite_matrix[y * 3 + 1][x * 3 + 2] = "wall-right"
                if sud:
                    self.sprite_matrix[y * 3 + 2][x * 3 + 1] = "wall-bottom"
                if ouest:
                    self.sprite_matrix[y * 3 + 1][x * 3] = "wall-left"

                # Coins
                if nord and ouest:
                    self.sprite_matrix[y * 3][x * 3] = (
                        "corner-jonction-top-left"
                    )
                elif nord:
                    self.sprite_matrix[y * 3][x * 3] = "wall-top"
                elif ouest:
                    self.sprite_matrix[y * 3][x * 3] = "wall-left"

                # Haut-droit : Nord & Est
                if nord and est:
                    self.sprite_matrix[y * 3][x * 3 + 2] = (
                        "corner-jonction-top-right"
                    )
                elif nord:
                    self.sprite_matrix[y * 3][x * 3 + 2] = "wall-top"
                elif est:
                    self.sprite_matrix[y * 3][x * 3 + 2] = "wall-right"

                # Bas-gauche : Sud & Ouest
                if sud and ouest:
                    self.sprite_matrix[y * 3 + 2][x * 3] = (
                        "corner-jonction-bottom-left"
                    )
                elif sud:
                    self.sprite_matrix[y * 3 + 2][x * 3] = "wall-bottom"
                elif ouest:
                    self.sprite_matrix[y * 3 + 2][x * 3] = "wall-left"

                # Bas-droit : Sud & Est
                if sud and est:
                    self.sprite_matrix[y * 3 + 2][x * 3 + 2] = (
                        "corner-jonction-bottom-right"
                    )
                elif sud:
                    self.sprite_matrix[y * 3 + 2][x * 3 + 2] = "wall-bottom"
                elif est:
                    self.sprite_matrix[y * 3 + 2][x * 3 + 2] = "wall-right"

                # Fermeture du wall
                last_x = len(self.map[0]) - 1
                last_y = len(self.map) - 1

                # ==========================================
                # Fermeture des murs horizontaux (nord/sud)
                # ==========================================

                if x > 0 and nord and not self.map[y][x - 1] & 1:
                    if self.map[y][x - 1] & (1 << 1):
                        self.sprite_matrix[y * 3][x * 3] = (
                            "corner-jonction-top-left"
                        )
                    elif self.map[y - 1][x - 1] & (1 << 1):
                        self.sprite_matrix[y * 3][x * 3] = "wall-top"
                    else:
                        # On met le mur NORD jusqu'au bout, on décale le coin dans la case voisine
                        self.sprite_matrix[y * 3][x * 3] = "wall-top"
                        self.sprite_matrix[y * 3][x * 3 - 1] = (
                            "corner-bottom-left"
                        )

                if x > 0 and sud and not self.map[y][x - 1] & (1 << 2):
                    if self.map[y][x - 1] & (1 << 1):
                        self.sprite_matrix[y * 3 + 2][x * 3] = (
                            "corner-jonction-bottom-left"
                        )
                    elif self.map[y + 1][x - 1] & (1 << 1):
                        self.sprite_matrix[y * 3 + 2][x * 3] = "wall-bottom"
                    else:
                        self.sprite_matrix[y * 3 + 2][x * 3] = "wall-bottom"
                        self.sprite_matrix[y * 3 + 2][x * 3 - 1] = (
                            "corner-top-left"
                        )

                if x < last_x and nord and not self.map[y][x + 1] & 1:
                    if self.map[y][x + 1] & (1 << 3):
                        self.sprite_matrix[y * 3][x * 3 + 2] = (
                            "corner-jonction-top-right"
                        )
                    elif self.map[y - 1][x + 1] & (1 << 3):
                        self.sprite_matrix[y * 3][x * 3 + 2] = "wall-top"
                    else:
                        self.sprite_matrix[y * 3][x * 3 + 2] = "wall-top"
                        self.sprite_matrix[y * 3][x * 3 + 3] = (
                            "corner-bottom-right"
                        )

                if x < last_x and sud and not self.map[y][x + 1] & (1 << 2):
                    if self.map[y][x + 1] & (1 << 3):
                        self.sprite_matrix[y * 3 + 2][x * 3 + 2] = (
                            "corner-jonction-bottom-right"
                        )
                    elif self.map[y + 1][x + 1] & (1 << 3):
                        self.sprite_matrix[y * 3 + 2][x * 3 + 2] = (
                            "wall-bottom"
                        )
                    else:
                        self.sprite_matrix[y * 3 + 2][x * 3 + 2] = (
                            "wall-bottom"
                        )
                        self.sprite_matrix[y * 3 + 2][x * 3 + 3] = (
                            "corner-top-right"
                        )

                # ==========================================
                # Fermeture des murs verticaux (est/ouest)
                # ==========================================

                if y > 0 and ouest and not self.map[y - 1][x] & (1 << 3):
                    if self.map[y - 1][x] & (1 << 2):
                        self.sprite_matrix[y * 3][x * 3] = (
                            "corner-jonction-top-left"
                        )
                    elif self.map[y - 1][x - 1] & (1 << 2):
                        self.sprite_matrix[y * 3][x * 3] = "wall-left"
                    else:
                        self.sprite_matrix[y * 3][x * 3] = "wall-left"
                        self.sprite_matrix[y * 3 - 1][x * 3] = (
                            "corner-top-right"
                        )

                if y > 0 and est and not self.map[y - 1][x] & (1 << 1):
                    if self.map[y - 1][x] & (1 << 2):
                        self.sprite_matrix[y * 3][x * 3 + 2] = (
                            "corner-jonction-top-right"
                        )
                    elif self.map[y - 1][x + 1] & (1 << 2):
                        self.sprite_matrix[y * 3][x * 3 + 2] = "wall-right"
                    else:
                        self.sprite_matrix[y * 3][x * 3 + 2] = "wall-right"
                        self.sprite_matrix[y * 3 - 1][x * 3 + 2] = (
                            "corner-top-left"
                        )

                if y < last_y and ouest and not self.map[y + 1][x] & (1 << 3):
                    if self.map[y + 1][x] & 1:
                        self.sprite_matrix[y * 3 + 2][x * 3] = (
                            "corner-jonction-bottom-left"
                        )
                    elif self.map[y + 1][x - 1] & 1:
                        self.sprite_matrix[y * 3 + 2][x * 3] = "wall-left"
                    else:
                        self.sprite_matrix[y * 3 + 2][x * 3] = "wall-left"
                        self.sprite_matrix[y * 3 + 3][x * 3] = (
                            "corner-bottom-right"
                        )

                if y < last_y and est and not self.map[y + 1][x] & (1 << 1):
                    if self.map[y + 1][x] & 1:
                        self.sprite_matrix[y * 3 + 2][x * 3 + 2] = (
                            "corner-jonction-bottom-right"
                        )
                    elif self.map[y + 1][x + 1] & 1:
                        self.sprite_matrix[y * 3 + 2][x * 3 + 2] = "wall-right"
                    else:
                        self.sprite_matrix[y * 3 + 2][x * 3 + 2] = "wall-right"
                        self.sprite_matrix[y * 3 + 3][x * 3 + 2] = (
                            "corner-bottom-left"
                        )
                if (
                    not sud
                    and not ouest
                    and x > 0
                    and y < last_y
                    and self.map[y][x - 1] & (1 << 2)
                    and self.map[y + 1][x] & (1 << 3)
                ):
                    self.sprite_matrix[y * 3 + 2][x * 3] = "corner-top-right"

                # Raccord Bas-Droit
                if (
                    not sud
                    and not est
                    and x < last_x
                    and y < last_y
                    and self.map[y][x + 1] & (1 << 2)
                    and self.map[y + 1][x] & (1 << 1)
                ):
                    self.sprite_matrix[y * 3 + 2][x * 3 + 2] = (
                        "corner-top-left"
                    )

                # Raccord Haut-Gauche
                if (
                    not nord
                    and not ouest
                    and x > 0
                    and y > 0
                    and self.map[y][x - 1] & 1
                    and self.map[y - 1][x] & (1 << 3)
                ):
                    self.sprite_matrix[y * 3][x * 3] = "corner-bottom-right"

                # Raccord Haut-Droit
                if (
                    not nord
                    and not est
                    and x < last_x
                    and y > 0
                    and self.map[y][x + 1] & 1
                    and self.map[y - 1][x] & (1 << 1)
                ):
                    self.sprite_matrix[y * 3][x * 3 + 2] = "corner-bottom-left"

                x += 1

        self.logic_matrix = []
        for y, row in enumerate(self.sprite_matrix):
            logic_row = []
            for x, cell_value in enumerate(row):
                if cell_value != "":
                    logic_row.append(PacmanCell.WALL)
                else:
                    logic_row.append(PacmanCell.PACGUM)
            self.logic_matrix.append(logic_row)

    def generate_map(self, seed: int = 0) -> None:
        self.generator.generate()
        self.map = self.generator.maze
        self.break_dead_ends(self.map)

        self.maze_to_matrix()

        for y, row in enumerate(self.logic_matrix):
            for x, cell_type in enumerate(row):
                base_x = x * self.TILE_SIZE
                base_y = y * self.TILE_SIZE

                if cell_type == PacmanCell.WALL:
                    sprite_val = self.sprite_matrix[y][x]
                    wall = Entity(f"wall_{x}_{y}")
                    wall.add_component(Position(base_x, base_y))
                    wall.add_component(Sprites([sprite_val]))

                    self.engine.add_single_entity(wall)

                elif cell_type == PacmanCell.PACGUM:
                    pacgum = Entity(f"pacgum_{x}_{y}")
                    pacgum.add_component(Position(base_x, base_y))

                    start = 1
                    end = (self.settings.map_width * 3) - 2
                    if (x == end or x == start) and (y == start or y == end):
                        pacgum.add_component(
                            Sprites(
                                ["super-pacgum-cell", "no-pacgum-cell"], 0.2
                            )
                        )
                        col = Collision("super_pacgum")
                    else:
                        pacgum.add_component(Sprites(["pacgum-cell"]))
                        col = Collision("pacgum")

                    hb = Hitbox(
                        2 * self.scale,
                        2 * self.scale,
                        3 * self.scale,
                        3 * self.scale,
                    )

                    pacgum.add_component(col)
                    pacgum.add_component(hb)

                    self.engine.add_single_entity(pacgum)

    def get_maze_cell_by_position(self, position: Position) -> tuple[int, int]:
        tile_size = 8 * self.settings.scale
        return (round(position.x / tile_size), round(position.y / tile_size))
