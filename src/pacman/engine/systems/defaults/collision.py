import itertools

from pacman.engine.components.defaults import Collision, Hitbox, Position
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.events.event import Event
from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources


class CollisionEvent(Event):
    def __init__(self, entity_a, entity_b):
        self.entity_a = entity_a
        self.entity_b = entity_b


class CollisionSystem(System):
    def __init__(self, ressources: Ressources):
        super().__init__([Position, Collision, Hitbox])
        self.ressources = ressources
        self.events = self.ressources.events

    def run(self) -> None:
        movers = []
        statics = []

        for subscriber in self.subscribers:
            if subscriber.check_component(Velocity):
                movers.append(
                    (
                        subscriber.get_component(Position),
                        subscriber.get_component(Hitbox),
                        subscriber.get_component(Collision),
                    )
                )
            else:
                statics.append(
                    (
                        subscriber.get_component(Position),
                        subscriber.get_component(Hitbox),
                        subscriber.get_component(Collision),
                    )
                )

        for m_pos, m_hit, m_col in movers:
            for s_pos, s_hit, s_col in statics:
                if m_col.tag == s_col.tag:
                    continue

                if (
                    m_pos.x + m_hit.padding_x + m_hit.width >= s_pos.x
                    and m_pos.x <= s_pos.x + s_hit.padding_x + s_hit.width
                    and m_pos.y + m_hit.padding_y + m_hit.height >= s_pos.y
                    and m_pos.y <= s_pos.y + s_hit.padding_y + s_hit.height
                ):
                    if s_col.tag in m_col.collision_map:
                        m_col.collision_map[s_col.tag]()
                    elif m_col.tag in s_col.collision_map:
                        s_col.collision_map[m_col.tag]()

        for first, second in itertools.combinations(movers, 2):
            f_pos, f_hit, f_col = first
            s_pos, s_hit, s_col = second

            if f_col.tag == s_col.tag:
                continue

            if (
                f_pos.x + f_hit.padding_x + f_hit.width >= s_pos.x
                and f_pos.x <= s_pos.x + s_hit.padding_x + s_hit.width
                and f_pos.y + f_hit.padding_y + f_hit.height >= s_pos.y
                and f_pos.y <= s_pos.y + s_hit.padding_y + s_hit.height
            ):
                if s_col.tag in f_col.collision_map:
                    f_col.collision_map[s_col.tag]()
                elif f_col.tag in s_col.collision_map:
                    s_col.collision_map[f_col.tag]()
