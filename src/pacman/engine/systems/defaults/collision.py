from pacman.engine.systems.system import System
from pacman.engine.components.defaults import Position, Collision, Hitbox
import itertools

class CollisionSystem(System):
    def __init__(self, ressources: dict | None):
        super().__init__([Position, Collision])
        self.ressources = ressources

    def run(self) -> None:
        for first, second in itertools.combinations(self.subscribers, 2):
            f_pos = first.get_component(Position)
            s_pos = second.get_component(Position)
            f_hit = first.get_component(Hitbox)
            s_hit = second.get_component(Hitbox)
            f_col = first.get_component(Collision)
            s_col = second.get_component(Collision)

            #print(f"tag 1: {f_col.tag}, tag 2: {s_col.tag}")
            if s_col.tag == f_col.tag:
                continue

            if (
                f_pos.x + f_hit.width >= s_pos.x and
                f_pos.x <= s_pos.x + s_hit.width and
                f_pos.y + f_hit.height >= s_pos.y and
                f_pos.y <= s_pos.y + s_hit.height
            ):
                if s_col.tag in f_col.collision_map:
                    f_col.collision_map[s_col.tag]()
                elif f_col.tag in s_col.collision_map:
                    s_col.collision_map[f_col.tag]()


