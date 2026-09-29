import pyray as pr

from pacman.engine.components.defaults import KeyHook
from pacman.engine.events.event import Event
from pacman.engine.systems.system import System
from pacman.game.ressources import Ressources


class KeyPressEvent(Event):
    def __init__(self, key: pr.KeyboardKey) -> None:
        self.key = key


class KeySystem(System):
    def __init__(self, ressources: Ressources):
        super().__init__([KeyHook])
        self.ressources = ressources

    def run(self) -> None:
        for subscriber in self.subscribers:
            key_hook = subscriber.get_component(KeyHook)

            for key in key_hook.keys:
                if pr.is_key_pressed(key):
                    self.ressources.events.push(KeyPressEvent(key))
