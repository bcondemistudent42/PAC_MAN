import io
from dataclasses import dataclass
from typing import cast

import numpy as np
import pyray as pr
from PIL import Image


@dataclass
class SpriteSheetPos:
    x: int
    y: int
    height: int
    width: int


class SpriteService:
    """Loads named sprites from one or more sprite sheets."""

    def __init__(
        self, spritesheet: str, sprite_config: dict[str, SpriteSheetPos]
    ) -> None:
        self.map: dict[str, pr.Texture] = {}
        self.add_spritesheet(spritesheet, sprite_config)

    def add_spritesheet(
        self, spritesheet: str, sprite_config: dict[str, SpriteSheetPos]
    ) -> None:
        image = Image.open(spritesheet).convert("RGBA")
        image_array = np.array(image)

        for sprite_name, position in sprite_config.items():
            sprite_image = image_array[
                position.y : position.y + position.height,
                position.x : position.x + position.width,
            ].copy()
            mask = (sprite_image[:, :, :3] == [0, 0, 0]).all(axis=-1)
            sprite_image[mask, 3] = 0

            buffer = io.BytesIO()
            Image.fromarray(sprite_image).save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            loaded_image = pr.load_image_from_memory(
                ".png", cast(str, image_bytes), len(image_bytes)
            )
            self.map[sprite_name] = pr.load_texture_from_image(loaded_image)
            pr.unload_image(loaded_image)

    def get_sprite(self, sprite: str) -> pr.Texture:
        return self.map[sprite]

    def exit_sprites(self) -> None:
        for texture in self.map.values():
            pr.unload_texture(texture)
        self.map.clear()
