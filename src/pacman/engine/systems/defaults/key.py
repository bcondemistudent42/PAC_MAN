import pyray as pr

from ...components.defaults import KeyHook
from ...components.defaults.sprites import Sprites
from ...events.event import Event
from ...resources import Resources
from ..system import System


class KeyPressEvent(Event):
    def __init__(self, key: pr.KeyboardKey) -> None:
        self.key = key


class KeySystem(System):
    def __init__(self, resources: Resources):
        super().__init__([KeyHook, Sprites])
        self.resources = resources

    def run(self) -> None:
        for subscriber in self.subscribers:
            key_hook = subscriber.get_component(KeyHook)

            for key in key_hook.keys:
                if pr.is_key_pressed(key):
                    self.resources.events.push(KeyPressEvent(key))
