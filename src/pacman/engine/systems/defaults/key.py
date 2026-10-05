import pyray as pr

from pacman.engine.components.defaults import KeyHook
from pacman.engine.components.defaults.sprites import Sprites
from pacman.engine.events.event import Event
from pacman.engine.systems.system import System
from pacman.game.components.dead import Dead
from pacman.game.resources import resources


class KeyPressEvent(Event):
    def __init__(self, key: pr.KeyboardKey) -> None:
        self.key = key


class KeySystem(System):
    def __init__(self, resources: resources):
        super().__init__([KeyHook, Sprites])
        self.resources = resources

    def run(self) -> None:
        for subscriber in self.subscribers:
            if subscriber.get_component(Dead).dead:
                return
            key_hook = subscriber.get_component(KeyHook)

            for key in key_hook.keys:
                if pr.is_key_pressed(key):
                    self.resources.events.push(KeyPressEvent(key))
