import itertools

from pacman.engine.components.defaults import Collision, Hitbox, Position
from pacman.engine.components.defaults.velocity import Velocity
from pacman.engine.components.entity import Entity
from pacman.engine.events.event import Event
from pacman.engine.systems.system import System
from pacman.game.resources import resources


class CollisionEvent(Event):
    def __init__(self, entities: dict[str, Entity]):
        self.entities = entities


class CollisionSystem(System):
    def __init__(self, resources: resources):
        super().__init__([Position, Collision, Hitbox])
        self.resources = resources
        self.events = self.resources.events

    def run(self) -> None:
        movers = []
        statics = []
        to_remove = []

        for subscriber in self.subscribers:
            if not (
                Collision in subscriber.components
                and Hitbox in subscriber.components
            ):
                to_remove.append(subscriber)
                continue

            if subscriber.check_component(Velocity):
                movers.append(
                    (
                        subscriber.get_component(Position),
                        subscriber.get_component(Hitbox),
                        subscriber.get_component(Collision),
                        subscriber,
                    )
                )
            else:
                statics.append(
                    (
                        subscriber.get_component(Position),
                        subscriber.get_component(Hitbox),
                        subscriber.get_component(Collision),
                        subscriber,
                    )
                )

        for m_pos, m_hit, m_col, m_sub in movers:
            for s_pos, s_hit, s_col, s_sub in statics:
                if m_col.tag == s_col.tag:
                    continue

                if (
                    m_pos.x + m_hit.padding_x + m_hit.width >= s_pos.x
                    and m_pos.x <= s_pos.x + s_hit.padding_x + s_hit.width
                    and m_pos.y + m_hit.padding_y + m_hit.height >= s_pos.y
                    and m_pos.y <= s_pos.y + s_hit.padding_y + s_hit.height
                ):
                    self.events.push(
                        CollisionEvent(
                            entities={s_col.tag: s_sub, m_col.tag: m_sub}
                        )
                    )

        for first, second in itertools.combinations(movers, 2):
            f_pos, f_hit, f_col, f_sub = first
            s_pos, s_hit, s_col, s_sub = second

            if f_col.tag == s_col.tag:
                continue

            if (
                f_pos.x + f_hit.padding_x + f_hit.width >= s_pos.x
                and f_pos.x <= s_pos.x + s_hit.padding_x + s_hit.width
                and f_pos.y + f_hit.padding_y + f_hit.height >= s_pos.y
                and f_pos.y <= s_pos.y + s_hit.padding_y + s_hit.height
            ):
                self.events.push(
                    CollisionEvent(
                        entities={s_col.tag: s_sub, f_col.tag: f_sub}
                    )
                )

        for elem in to_remove:
            self.subscribers.remove(elem)
