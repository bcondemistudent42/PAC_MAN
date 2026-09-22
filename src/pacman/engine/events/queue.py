from collections import deque

from pacman.engine.events.event import Event


class EventsQueue:
    def __init__(self) -> None:
        self.events: deque[Event] = deque([])

    def push(self, event: Event) -> None:
        self.events.append(event)
