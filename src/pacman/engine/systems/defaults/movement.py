from pacman.engine.systems.system import System
from pacman.engine.components.defaults import Position, Velocity

class MovementSystem(System):
    def __init__(self, ressources: dict):
        super().__init__([Position, Velocity])
        self.ressources = ressources

    @staticmethod
    def add_movement(Position, Velocity):
        return (Position.x + Velocity.x, Position.y + Velocity.y)

    def run(self):
        for subscriber in self.subscribers:
            actu_position = subscriber.get_component(Position)
            velo = subscriber.get_component(Velocity)

            actu_position.x += velo.x
            actu_position.y += velo.y

            if actu_position.x > 270:
                from pacman.death import make_death, DeathSprites
                make_death(subscriber, DeathSprites.PACMAN.value)

