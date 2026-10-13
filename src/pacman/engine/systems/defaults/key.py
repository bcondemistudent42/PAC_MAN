import pyray as pr

from ...components.defaults import KeyHook
from ...components.defaults.sprites import Sprites
from ...events.event import Event
from ...resources import Resources
from ..system import System


class KeyPressEvent(Event):
    """Represent a keyboard key pressed during the current frame."""

    def __init__(self, key: pr.KeyboardKey) -> None:
        """Create a key press event.

        Args:
            key: Keyboard key that was pressed.
        """
        self.key = key


class KeySystem(System):
    """Translate configured keyboard hooks into key press events."""

    def __init__(self, resources: Resources):
        """Create a keyboard polling system."""
        super().__init__([KeyHook, Sprites])
        self.resources = resources

    def run(self) -> None:
        """Poll hooked keys and enqueue events for newly pressed keys.

        Only keys mapped by a subscriber's ``KeyHook`` component are checked.
        """
        if self.resources.frozen:
            return

        for subscriber in self.subscribers:
            key_hook = subscriber.get_component(KeyHook)

            for key in key_hook.keys:
                if pr.is_key_pressed(key):
                    self.resources.events.push(KeyPressEvent(key))
