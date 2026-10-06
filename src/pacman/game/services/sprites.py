import io
from dataclasses import dataclass

import numpy as np
import pyray as pr
from PIL import Image


@dataclass
class SpriteSheetPos:
    x: int
    y: int
    height: int
    width: int


config = {
    "pacman-right-1": SpriteSheetPos(x=456, y=0, width=16, height=16),
    "pacman-right-2": SpriteSheetPos(x=472, y=0, width=16, height=16),
    "pacman-right-3": SpriteSheetPos(x=488, y=0, width=16, height=16),
    "pacman-left-1": SpriteSheetPos(x=456, y=16, width=16, height=16),
    "pacman-left-2": SpriteSheetPos(x=472, y=16, width=16, height=16),
    "pacman-left-3": SpriteSheetPos(x=488, y=16, width=16, height=16),
    "pacman-top-1": SpriteSheetPos(x=456, y=32, width=16, height=16),
    "pacman-top-2": SpriteSheetPos(x=472, y=32, width=16, height=16),
    "pacman-top-3": SpriteSheetPos(x=488, y=32, width=16, height=16),
    "pacman-bottom-1": SpriteSheetPos(x=456, y=48, width=16, height=16),
    "pacman-bottom-2": SpriteSheetPos(x=472, y=48, width=16, height=16),
    "pacman-bottom-3": SpriteSheetPos(x=488, y=48, width=16, height=16),
    "pacman-dead-1": SpriteSheetPos(x=504, y=0, width=16, height=16),
    "pacman-dead-2": SpriteSheetPos(x=520, y=0, width=16, height=16),
    "pacman-dead-3": SpriteSheetPos(x=536, y=0, width=16, height=16),
    "pacman-dead-4": SpriteSheetPos(x=552, y=0, width=16, height=16),
    "pacman-dead-5": SpriteSheetPos(x=568, y=0, width=16, height=16),
    "pacman-dead-6": SpriteSheetPos(x=584, y=0, width=16, height=16),
    "pacman-dead-7": SpriteSheetPos(x=600, y=0, width=16, height=16),
    "pacman-dead-8": SpriteSheetPos(x=616, y=0, width=16, height=16),
    "pacman-dead-9": SpriteSheetPos(x=632, y=0, width=16, height=16),
    "pacman-dead-10": SpriteSheetPos(x=648, y=0, width=16, height=16),
    "pacman-dead-11": SpriteSheetPos(x=664, y=0, width=16, height=16),
    "blinky-right-1": SpriteSheetPos(x=456, y=64, width=16, height=16),
    "blinky-right-2": SpriteSheetPos(x=472, y=64, width=16, height=16),
    "blinky-left-1": SpriteSheetPos(x=488, y=64, width=16, height=16),
    "blinky-left-2": SpriteSheetPos(x=504, y=64, width=16, height=16),
    "blinky-top-1": SpriteSheetPos(x=520, y=64, width=16, height=16),
    "blinky-top-2": SpriteSheetPos(x=536, y=64, width=16, height=16),
    "blinky-bottom-1": SpriteSheetPos(x=552, y=64, width=16, height=16),
    "blinky-bottom-2": SpriteSheetPos(x=568, y=64, width=16, height=16),
    "blue-ghost-1": SpriteSheetPos(x=584, y=64, width=16, height=16),
    "blue-ghost-2": SpriteSheetPos(x=600, y=64, width=16, height=16),
    "white-ghost-1": SpriteSheetPos(x=616, y=64, width=16, height=16),
    "white-ghost-2": SpriteSheetPos(x=632, y=64, width=16, height=16),
    "pinky-right-1": SpriteSheetPos(x=456, y=80, width=16, height=16),
    "pinky-right-2": SpriteSheetPos(x=472, y=80, width=16, height=16),
    "pinky-left-1": SpriteSheetPos(x=488, y=80, width=16, height=16),
    "pinky-left-2": SpriteSheetPos(x=504, y=80, width=16, height=16),
    "pinky-top-1": SpriteSheetPos(x=520, y=80, width=16, height=16),
    "pinky-top-2": SpriteSheetPos(x=536, y=80, width=16, height=16),
    "pinky-bottom-1": SpriteSheetPos(x=552, y=80, width=16, height=16),
    "pinky-bottom-2": SpriteSheetPos(x=568, y=80, width=16, height=16),
    "ghost-eyes-right": SpriteSheetPos(x=584, y=80, width=16, height=16),
    "ghost-eyes-left": SpriteSheetPos(x=600, y=80, width=16, height=16),
    "ghost-eyes-top": SpriteSheetPos(x=616, y=80, width=16, height=16),
    "ghost-eyes-bottom": SpriteSheetPos(x=532, y=80, width=16, height=16),
    "inky-right-1": SpriteSheetPos(x=456, y=96, width=16, height=16),
    "inky-right-2": SpriteSheetPos(x=472, y=96, width=16, height=16),
    "inky-left-1": SpriteSheetPos(x=488, y=96, width=16, height=16),
    "inky-left-2": SpriteSheetPos(x=504, y=96, width=16, height=16),
    "inky-top-1": SpriteSheetPos(x=520, y=96, width=16, height=16),
    "inky-top-2": SpriteSheetPos(x=536, y=96, width=16, height=16),
    "inky-bottom-1": SpriteSheetPos(x=552, y=96, width=16, height=16),
    "inky-bottom-2": SpriteSheetPos(x=568, y=96, width=16, height=16),
    "clyde-right-1": SpriteSheetPos(x=456, y=113, width=16, height=16),
    "clyde-right-2": SpriteSheetPos(x=472, y=113, width=16, height=16),
    "clyde-left-1": SpriteSheetPos(x=488, y=113, width=16, height=16),
    "clyde-left-2": SpriteSheetPos(x=504, y=113, width=16, height=16),
    "clyde-top-1": SpriteSheetPos(x=520, y=113, width=16, height=16),
    "clyde-top-2": SpriteSheetPos(x=536, y=113, width=16, height=16),
    "clyde-bottom-1": SpriteSheetPos(x=552, y=113, width=16, height=16),
    "clyde-bottom-2": SpriteSheetPos(x=568, y=113, width=16, height=16),
    "left-top-map-corner": SpriteSheetPos(x=0, y=0, width=8, height=8),
    "left-bottom-map-corner": SpriteSheetPos(x=0, y=240, width=8, height=8),
    "right-top-map-corner": SpriteSheetPos(x=216, y=0, width=8, height=8),
    "right-bottom-map-corner": SpriteSheetPos(x=216, y=240, width=8, height=8),
    "wall-bottom": SpriteSheetPos(x=24, y=16, width=8, height=8),
    "wall-top": SpriteSheetPos(x=24, y=32, width=8, height=8),
    "wall-right": SpriteSheetPos(x=16, y=24, width=8, height=8),
    "wall-left": SpriteSheetPos(x=40, y=24, width=8, height=8),
    "corner-top-left": SpriteSheetPos(x=16, y=16, width=8, height=8),
    "corner-top-right": SpriteSheetPos(x=40, y=16, width=8, height=8),
    "corner-bottom-left": SpriteSheetPos(x=16, y=32, width=8, height=8),
    "corner-bottom-right": SpriteSheetPos(x=40, y=32, width=8, height=8),
    "corner-jonction-bottom-left": SpriteSheetPos(x=64, y=72, width=8, height=8),
    "corner-jonction-top-left": SpriteSheetPos(x=112, y=152, width=8, height=8),
    "corner-jonction-bottom-right": SpriteSheetPos(x=152, y=72, width=8, height=8),
    "corner-jonction-top-right": SpriteSheetPos(x=104, y=152, width=8, height=8),
    "pacgum-cell": SpriteSheetPos(x=8, y=8, width=8, height=8),
    "super-pacgum-cell": SpriteSheetPos(x=8, y=24, width=8, height=8),
    "no-pacgum-cell": SpriteSheetPos(x=232, y=20, width=8, height=8),
}


config_spritesheet_2 = {
    "creeper-1": SpriteSheetPos(x=0, y=0, width=8, height=8),
    "creeper-2": SpriteSheetPos(x=8, y=0, width=8, height=8),
    "creeper-3": SpriteSheetPos(x=16, y=0, width=8, height=8),
    "creeper-4": SpriteSheetPos(x=0, y=8, width=8, height=8),
    "creeper-5": SpriteSheetPos(x=8, y=8, width=8, height=8),
    "creeper-6": SpriteSheetPos(x=16, y=8, width=8, height=8),
    "creeper-7": SpriteSheetPos(x=0, y=16, width=8, height=8),
    "creeper-8": SpriteSheetPos(x=8, y=16, width=8, height=8),
    "creeper-9": SpriteSheetPos(x=16, y=16, width=8, height=8),
}


class SpriteService:
    def __init__(self, spritesheet: str, map: dict[str, SpriteSheetPos]) -> None:
        self.spritesheet = spritesheet
        self.config_map = map
        self.img = Image.open(spritesheet).convert("RGBA")
        self.img_array = np.array(self.img)
        self.map = {}

        self.init_sprites()

    def add_spritesheet(self, spritesheet: str, map: dict[str, SpriteSheetPos]) -> None:
        self.spritesheet = spritesheet
        self.config_map = map
        self.img = Image.open(spritesheet).convert("RGBA")
        self.img_array = np.array(self.img)

        self.init_sprites()

    def init_sprites(self) -> None:
        for sprite, pos in self.config_map.items():
            sprite_raw = self.img_array[
                pos.y : pos.y + pos.height, pos.x : pos.x + pos.width
            ]

            mask = (sprite_raw[:, :, :3] == [0, 0, 0]).all(axis=-1)
            sprite_raw[mask, 3] = 0

            result = Image.fromarray(sprite_raw)
            bytes_arr = io.BytesIO()
            result.save(bytes_arr, format="PNG")
            raw_img = bytes_arr.getvalue()
            img = pr.load_image_from_memory(".png", raw_img, len(raw_img))

            self.map[sprite] = pr.load_texture_from_image(img)

            pr.unload_image(img)

    def exit_sprites(self) -> None:
        for image in self.map.values():
            pr.unload_image(image)

    def get_sprite(self, sprite: str) -> pr.Image:
        return self.map[sprite]


if __name__ == "__main__":
    manager = SpriteService("spritesheet.png", config)
    manager.init_sprites()
