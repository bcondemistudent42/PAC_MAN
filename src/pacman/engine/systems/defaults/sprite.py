import pyray as pr

from pacman.engine.components.defaults import Position, Sprites
from pacman.engine.systems.system import System
from pacman.services.sprites import SpriteService


class SpriteSystem(System):
    def __init__(self, ressources: dict):
        super().__init__([Position, Sprites])
        self.ressources = ressources

    def run(self):
        self.sprite_service = self.ressources[SpriteService]
        self.SCALE = self.ressources["scale"]
        tile_size = 8 * self.SCALE

        for each_subscribed in self.subscribers:
            sprite_component = each_subscribed.get_component(Sprites)
            position_component = each_subscribed.get_component(Position)

            sprite_component.frame += pr.get_frame_time()

            if sprite_component.frame >= sprite_component.cooldown:
                if sprite_component.sprite_index < len(sprite_component.sprites) - 1:
                    sprite_component.sprite_index += 1
                else:
                    sprite_component.sprite_index = 0
                sprite_component.frame = 0

            index = sprite_component.sprite_index
            x = position_component.x
            y = position_component.y

            texture = self.sprite_service.get_sprite(sprite_component.sprites[index])

            offset_x = (tile_size - texture.width * self.SCALE) / 2
            offset_y = (tile_size - texture.height * self.SCALE) / 2

            pr.draw_texture_ex(
                texture,
                pr.Vector2(x + offset_x, y + offset_y),
                0.0,
                self.SCALE,
                pr.WHITE,
            )
