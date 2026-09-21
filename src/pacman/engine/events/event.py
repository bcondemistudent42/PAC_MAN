import pyray as pr


class Event: ...


class KeyPressEvent(Event):
    def __init__(self, key: pr.KeyboardKey):
        self.key = key
