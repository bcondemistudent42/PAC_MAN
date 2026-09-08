from pacman.engine.ecs import Component, Entity, Position, Velocity, Sprite


# tosee if good fault of bcondemi if not
import pyray as pr

class System:
    def __init__(self, components: list[type[Component]]):
        self.subscribers: list[Entity] = []
        self.required_components: list[type[Component]] = []

    def subscribe(self, entity: Entity):
        for component in self.required_components:
            if not component in entity.components:
                raise ValueError("A definir")

        self.subscribers.append(entity)


class MovementSystem(System):
    def __init__(self):
        super().__init__([Position, Velocity])

    @staticmethod
    def add_movement(Position, Velocity):
        return (Position.x + Velocity.x, Position.y + Velocity.y)

    def run(self):
        for subscriber in self.subscribers:
            actu_position = subscriber.components[Position]
            velo = subscriber.components[Velocity]
    
            print(f"Position actuelle {actu_position}")

            actu_position.x += velo.x
            actu_position.y += velo.y

            print(f"Nouvelle position: {actu_position}") 

class SpriteSystem(System):
    def __init__(self):
        super().__init__([Position, Sprite])

    # can name it just display
    def run(self):
        for each_subscribed in self.subscribers:
            img = pr.load_texture(each_subscribed.components[Sprite].img_path)

            x = each_subscribed.components[Position].x
            y = each_subscribed.components[Position].y

            pr.draw_texture(img, x, y, pr.WHITE)

