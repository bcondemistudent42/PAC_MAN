import pyray as pr

from pacman.engine.components.defaults import Position, Sprites
from pacman.game.components.scared import Scared
from pacman.engine.systems.system import System
from pacman.game.resources import resources


class SpriteSystem(System):
    def __init__(self, resources: resources):
        super().__init__([Position, Sprites])
        self.resources = resources

    def run(self):
        sprite_service = self.resources.sprite_service
        if sprite_service is None:
            raise RuntimeError("Sprite service is not initialized")

        scale = self.resources.scale
        tile_size = 8 * scale

        for each_subscribed in self.subscribers:
            sprite_component = each_subscribed.get_component(Sprites)
            position_component = each_subscribed.get_component(Position)

            if len(sprite_component.sprites) <= 0:
                continue

            sprite_component.frame += pr.get_frame_time()

            if sprite_component.cooldown and sprite_component.frame >= sprite_component.cooldown:
                if sprite_component.sprite_index < len(sprite_component.sprites) - 1:
                    sprite_component.sprite_index += 1
                else:
                    sprite_component.sprite_index = 0
                sprite_component.frame = 0

            index = sprite_component.sprite_index
            x = position_component.x
            y = position_component.y

            texture = sprite_service.get_sprite(sprite_component.sprites[index])
            if each_subscribed.check_component(Scared) and each_subscribed.get_component(Scared).scared:
                if (sprite_component.sprite_index) >= len(each_subscribed.get_component(Scared).sprites):
                    sprite_component.sprite_index = 0
                index = sprite_component.sprite_index
                texture = sprite_service.get_sprite(each_subscribed.get_component(Scared).sprites[index])

            offset_x = (tile_size - texture.width * scale) / 2
            offset_y = (tile_size - texture.height * scale) / 2

            pr.draw_texture_ex(
                texture,
                pr.Vector2(x + offset_x, y + offset_y),
                0.0,
                scale,
                pr.WHITE,
            )
