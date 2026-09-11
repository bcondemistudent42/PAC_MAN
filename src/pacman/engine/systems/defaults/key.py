from pacman.engine.systems.system import System
from pacman.engine.components.defaults import KeyHook
import pyray as pr

class KeySystem(System):
    def __init__(self, ressources: dict | None):
        super().__init__([KeyHook])
        self.ressources = ressources

    def run(self) -> None:
        for subscriber in self.subscribers:
            key_hook = subscriber.get_component(KeyHook)

            for key, on_press in key_hook.keys.items():
                if pr.is_key_pressed(key):
                    on_press() 
