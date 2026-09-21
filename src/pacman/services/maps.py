from mazegenerator import MazeGenerator

from pacman.engine import GameEngine
from pacman.engine.components.defaults.collision import Collision
from pacman.engine.components.defaults.hitbox import Hitbox
from pacman.engine.components.defaults.position import Position
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.components.entity import Entity
from pacman.engine.systems.defaults.collision import CollisionSystem


class PacmanMap:
    def __init__(
        self, engine: GameEngine, scale: float, map_width: int, map_height: int
    ) -> None:
        self.generator = MazeGenerator(size=(map_width, map_height), perfect=False, seed=engine.data_user.seed)

        self.TILE_SIZE = 8 * scale

        self.engine = engine
        self.map = []

    def maze_to_matrix(self) -> list[list[str]]:
        result = [
            ["" for _ in range(len(self.map[0]) * 3)] for _ in range(len(self.map) * 3)
        ]

        for y, line in enumerate(self.map):
            for x, hexa_rep in enumerate(line):
                cell = hexa_rep

                nord = bool(cell & 1)
                est = bool(cell & (1 << 1))
                sud = bool(cell & (1 << 2))
                ouest = bool(cell & (1 << 3))

                result[y * 3 + 1][x * 3 + 1] = ""  # Centre vide

                # Bords
                if nord:
                    result[y * 3][x * 3 + 1] = "wall-top"
                if est:
                    result[y * 3 + 1][x * 3 + 2] = "wall-right"
                if sud:
                    result[y * 3 + 2][x * 3 + 1] = "wall-bottom"
                if ouest:
                    result[y * 3 + 1][x * 3] = "wall-left"

                # Coins
                if nord and ouest:
                    result[y * 3][x * 3] = "corner-top-left"
                elif nord:
                    result[y * 3][x * 3] = "wall-top"
                elif ouest:
                    result[y * 3][x * 3] = "wall-left"

                # Haut-droit : Nord & Est
                if nord and est:
                    result[y * 3][x * 3 + 2] = "corner-top-right"
                elif nord:
                    result[y * 3][x * 3 + 2] = "wall-top"
                elif est:
                    result[y * 3][x * 3 + 2] = "wall-right"

                # Bas-gauche : Sud & Ouest
                if sud and ouest:
                    result[y * 3 + 2][x * 3] = "corner-bottom-left"
                elif sud:
                    result[y * 3 + 2][x * 3] = "wall-bottom"
                elif ouest:
                    result[y * 3 + 2][x * 3] = "wall-left"

                # Bas-droit : Sud & Est
                if sud and est:
                    result[y * 3 + 2][x * 3 + 2] = "corner-bottom-right"
                elif sud:
                    result[y * 3 + 2][x * 3 + 2] = "wall-bottom"
                elif est:
                    result[y * 3 + 2][x * 3 + 2] = "wall-right"

                # Fermeture du wall
                last_x = len(self.map[0]) - 1
                last_y = len(self.map) - 1
                # Fermeture des murs horizontaux (nord/sud), caps gauche/droite
                if x > 0 and nord and not self.map[y][x - 1] & 1:
                    if self.map[y][x - 1] & (1 << 1):  # Le voisin gauche a un mur Est
                        result[y * 3][x * 3] = "corner-top-left"
                    elif self.map[y - 1][x - 1] & (1 << 1):
                        result[y * 3][x * 3] = "wall-top"
                    else:
                        result[y * 3][x * 3] = "corner-bottom-left"

                if x > 0 and sud and not self.map[y][x - 1] & (1 << 2):
                    if self.map[y][x - 1] & (1 << 1):  # Le voisin gauche a un mur Est
                        result[y * 3 + 2][x * 3] = "corner-bottom-left"
                    elif self.map[y + 1][x - 1] & (1 << 1):
                        result[y * 3 + 2][x * 3] = "wall-bottom"
                    else:
                        result[y * 3 + 2][x * 3] = "corner-top-left"

                if x < last_x and nord and not self.map[y][x + 1] & 1:
                    if self.map[y][x + 1] & (1 << 3):  # Le voisin droit a un mur Ouest
                        result[y * 3][x * 3 + 2] = "corner-top-right"
                    elif self.map[y - 1][x + 1] & (1 << 3):
                        result[y * 3][x * 3 + 2] = "wall-top"
                    else:
                        result[y * 3][x * 3 + 2] = "corner-bottom-right"

                if x < last_x and sud and not self.map[y][x + 1] & (1 << 2):
                    if self.map[y][x + 1] & (1 << 3):  # Le voisin droit a un mur Ouest
                        result[y * 3 + 2][x * 3 + 2] = "corner-bottom-right"
                    elif self.map[y + 1][x + 1] & (1 << 3):
                        result[y * 3 + 2][x * 3 + 2] = "wall-bottom"
                    else:
                        result[y * 3 + 2][x * 3 + 2] = "corner-top-right"

                # Fermeture des murs verticaux (est/ouest), caps haut/bas
                if y > 0 and ouest and not self.map[y - 1][x] & (1 << 3):
                    if self.map[y - 1][x] & (1 << 2):  # Le voisin haut a un mur Sud
                        result[y * 3][x * 3] = "corner-top-left"
                    elif self.map[y - 1][x - 1] & (1 << 2):
                        result[y * 3][x * 3] = "wall-left"
                    else:
                        result[y * 3][x * 3] = "corner-top-right"

                if y > 0 and est and not self.map[y - 1][x] & (1 << 1):
                    if self.map[y - 1][x] & (1 << 2):  # Le voisin haut a un mur Sud
                        result[y * 3][x * 3 + 2] = "corner-top-right"
                    elif self.map[y - 1][x + 1] & (1 << 2):
                        result[y * 3][x * 3 + 2] = "wall-right"
                    else:
                        result[y * 3][x * 3 + 2] = "corner-top-left"

                if y < last_y and ouest and not self.map[y + 1][x] & (1 << 3):
                    if self.map[y + 1][x] & 1:  # Le voisin bas a un mur Nord
                        result[y * 3 + 2][x * 3] = "corner-bottom-left"
                    elif self.map[y + 1][x - 1] & 1:
                        result[y * 3 + 2][x * 3] = "wall-left"
                    else:
                        result[y * 3 + 2][x * 3] = "corner-bottom-right"

                if y < last_y and est and not self.map[y + 1][x] & (1 << 1):
                    if self.map[y + 1][x] & 1:  # Le voisin bas a un mur Nord
                        result[y * 3 + 2][x * 3 + 2] = "corner-bottom-right"
                    elif self.map[y + 1][x + 1] & 1:
                        result[y * 3 + 2][x * 3 + 2] = "wall-right"
                    else:
                        result[y * 3 + 2][x * 3 + 2] = "corner-bottom-left"

                if (
                    not sud
                    and not ouest
                    and x > 0
                    and y < last_y
                    and self.map[y][x - 1] & (1 << 2)
                    and self.map[y + 1][x] & (1 << 3)
                ):
                    result[y * 3 + 2][x * 3] = "corner-top-right"

                # Raccord Bas-Droit
                if (
                    not sud
                    and not est
                    and x < last_x
                    and y < last_y
                    and self.map[y][x + 1] & (1 << 2)
                    and self.map[y + 1][x] & (1 << 1)
                ):
                    result[y * 3 + 2][x * 3 + 2] = "corner-top-left"

                # Raccord Haut-Gauche
                if (
                    not nord
                    and not ouest
                    and x > 0
                    and y > 0
                    and self.map[y][x - 1] & 1
                    and self.map[y - 1][x] & (1 << 3)
                ):
                    result[y * 3][x * 3] = "corner-bottom-right"

                # Raccord Haut-Droit
                if (
                    not nord
                    and not est
                    and x < last_x
                    and y > 0
                    and self.map[y][x + 1] & 1
                    and self.map[y - 1][x] & (1 << 1)
                ):
                    result[y * 3][x * 3 + 2] = "corner-bottom-left"

                x += 1

        return result

    def generate_map(self, seed: int = 0) -> None:
        self.generator.generate()
        self.map = self.generator.maze

        sprite_matrix = self.maze_to_matrix()

        col_sys = next(
            sys for sys in self.engine.systems if isinstance(sys, CollisionSystem)
        )

        for y, row in enumerate(sprite_matrix):
            for x, cell_value in enumerate(row):
                base_x = x * self.TILE_SIZE
                base_y = y * self.TILE_SIZE

                if cell_value != "":
                    wall = Entity(f"wall_{x}_{y}")
                    wall.add_component(Position(base_x, base_y))
                    wall.add_component(Sprites([cell_value], 999999999999999999999999))
                    wall.add_component(Hitbox(int(self.TILE_SIZE), int(self.TILE_SIZE)))
                    col = Collision(cell_value, {})
                    wall.add_component(col)

                    self.engine.add_single_entity(wall)

                elif cell_value == "":
                    if (x % 3 == 1) and (y % 3 == 1):
                        pacgum = Entity(f"pacgum_{x}_{y}")
                        pacgum.add_component(Position(base_x, base_y))
                        pacgum.add_component(
                            Sprites(["pacgum-cell"], 999999999999999999999999)
                        )

                        def handle_pacman_pacgum_collision(target=pacgum) -> None:
                            target.get_component(Sprites).sprites = ["no-pacgum-cell"]
                            col_sys.unsubscribe(target)

                        col = Collision(
                            "pacgum", {"pacman": handle_pacman_pacgum_collision}
                        )
                        hb = Hitbox(2, 2, 3, 3)  # Add scale

                        pacgum.add_component(col)
                        pacgum.add_component(hb)

                        self.engine.add_single_entity(pacgum)
