from .event import Event


class EventsQueue:
    """Store events until they are consumed by the engine."""

    def __init__(self) -> None:
        """Initialize an empty event queue."""
        self.events: list[Event] = []

    def push(self, event: Event) -> None:
        """Append an event to the queue.

        Args:
            event: Event to append.
        """
        self.events.append(event)

    def drain(self) -> list[Event]:
        """Return all queued events and empty the queue."""
        events = self.events
        self.events = []
        return events
