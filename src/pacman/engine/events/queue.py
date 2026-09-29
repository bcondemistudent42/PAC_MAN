from pacman.engine.events.event import Event


class EventsQueue:
    def __init__(self) -> None:
        self.events: list[Event] = []

    def push(self, event: Event) -> None:
        self.events.append(event)

    def drain(self) -> list[Event]:
        events = self.events
        self.events = []
        return events
