from pacman.engine.systems.system import System
from pacman.engine.components.defaults import Position, Sprites
from pacman.services.sprites import SpriteService
import pyray as pr

class SpriteSystem(System):
    def __init__(self, ressources: dict):
        super().__init__([Position, Sprites])
        self.ressources = ressources
        self.sprite_service = self.ressources[SpriteService]

    def run(self):
        for each_subscribed in self.subscribers:
            sprite_component = each_subscribed.get_component(Sprites)
            position_component = each_subscribed.get_component(Position)

            sprite_component.frame += pr.get_frame_time()

            # print(f"{sprite_component.frame} >= {sprite_component.cooldown}")
            # print(f"{sprite_component.frame >= sprite_component.cooldown}")
            if sprite_component.frame >= sprite_component.cooldown:
                if (
                    sprite_component.sprite_index <
                    len(sprite_component.sprites) - 1
                ):
                    sprite_component.sprite_index += 1
                else:
                    sprite_component.sprite_index = 0
                sprite_component.frame = 0

            index = sprite_component.sprite_index
            x = position_component.x
            y = position_component.y


            pr.draw_texture_ex(
                self.ressources[SpriteService].get_sprite(
                    sprite_component.sprites[index]
                ),
                pr.Vector2(x, y),
                0.0,
                5.0,
                pr.WHITE
            )
