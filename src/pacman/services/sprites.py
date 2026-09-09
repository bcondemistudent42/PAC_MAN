from dataclasses import dataclass
import numpy as np
from PIL import Image
import pyray as pr
import io


@dataclass
class SpriteSheetPos:
    x: int
    y: int
    height: int
    width: int


class SpriteService:
    def __init__(
        self,
        spritesheet: str,
        map: dict[str, SpriteSheetPos]
    ) -> None:
        self.spritesheet = spritesheet
        self.config_map = map
        self.img = Image.open(spritesheet).convert("RGBA")
        self.img_array = np.array(self.img)
        self.map = {}

    def init_sprites(self) -> None:
        for sprite, pos in self.config_map.items():
            sprite_raw = self.img_array[
                pos.y:pos.y + pos.height,
                pos.x:pos.x + pos.width
            ]

            result = Image.fromarray(sprite_raw)
            bytes_arr = io.BytesIO()
            result.save(bytes_arr, format="PNG")
            raw_img = bytes_arr.getvalue()

            self.map[sprite] = (
                pr.load_image_from_memory("png", raw_img, len(raw_img))
            )

    def exit_sprites(self) -> None:
        for _, image in self.map.items():
            pr.unload_image(image)

    def get_sprite(self, sprite: str) -> pr.Image:
        return self.map[sprite]


if __name__ == "__main__":
    config = {
        "pacman-right-1": SpriteSheetPos(x=457, y=1, width=9, height=13),
        "pacman-right-2": SpriteSheetPos(x=473, y=1, width=13, height=13),
        "pacman-right-3": SpriteSheetPos(x=489, y=1, width=13, height=13),

        "pacman-left-1": SpriteSheetPos(x=462, y=17, width=9, height=13),
        "pacman-left-2": SpriteSheetPos(x=475, y=17, width=12, height=13),
        "pacman-left-3": SpriteSheetPos(x=490, y=17, width=13, height=13),

        "pacman-top-1": SpriteSheetPos(x=457, y=38, width=13, height=9),
        "pacman-top-2": SpriteSheetPos(x=473, y=35, width=12, height=13),
        "pacman-top-3": SpriteSheetPos(x=489, y=34, width=13, height=13),

        "pacman-bottom-1": SpriteSheetPos(x=457, y=49, width=13, height=9),
        "pacman-bottom-2": SpriteSheetPos(x=473, y=49, width=13, height=12),
        "pacman-bottom-3": SpriteSheetPos(x=489, y=49, width=13, height=13),

        "pacman-dead-1": SpriteSheetPos(x=505, y=3, width=13, height=9),
        "pacman-dead-2": SpriteSheetPos(x=520, y=4, width=15, height=8),
        "pacman-dead-3": SpriteSheetPos(x=536, y=6, width=15, height=6),
        "pacman-dead-4": SpriteSheetPos(x=552, y=7, width=15, height=5),
        "pacman-dead-5": SpriteSheetPos(x=568, y=8, width=15, height=5),
        "pacman-dead-6": SpriteSheetPos(x=584, y=8, width=15, height=6),
        "pacman-dead-7": SpriteSheetPos(x=601, y=8, width=13, height=7),
        "pacman-dead-8": SpriteSheetPos(x=619, y=8, width=9, height=7),
        "pacman-dead-9": SpriteSheetPos(x=637, y=8, width=5, height=7),
        "pacman-dead-10": SpriteSheetPos(x=655, y=8, width=1, height=6),
        "pacman-dead-11": SpriteSheetPos(x=666, y=6, width=11, height=10),

        "blinky-right-1": SpriteSheetPos(x=457, y=65, width=14, height=14),
        "blinky-right-2": SpriteSheetPos(x=473, y=65, width=14, height=14),
        "blinky-left-1": SpriteSheetPos(x=489, y=65, width=14, height=14),
        "blinky-left-2": SpriteSheetPos(x=505, y=65, width=14, height=14),
        "blinky-top-1": SpriteSheetPos(x=521, y=65, width=14, height=14),
        "blinky-top-2": SpriteSheetPos(x=537, y=65, width=14, height=14),
        "blinky-bottom-1": SpriteSheetPos(x=553, y=65, width=14, height=14),
        "blinky-bottom-2": SpriteSheetPos(x=569, y=65, width=14, height=14),

        "pinky-right-1": SpriteSheetPos(x=457, y=81, width=14, height=14),
        "pinky-right-2": SpriteSheetPos(x=473, y=81, width=14, height=14),
        "pinky-left-1": SpriteSheetPos(x=489, y=81, width=14, height=14),
        "pinky-left-2": SpriteSheetPos(x=505, y=81, width=14, height=14),
        "pinky-top-1": SpriteSheetPos(x=521, y=81, width=14, height=14),
        "pinky-top-2": SpriteSheetPos(x=537, y=81, width=14, height=14),
        "pinky-bottom-1": SpriteSheetPos(x=553, y=81, width=14, height=14),
        "pinky-bottom-2": SpriteSheetPos(x=569, y=81, width=14, height=14),

        "inky-right-1": SpriteSheetPos(x=457, y=97, width=14, height=14),
        "inky-right-2": SpriteSheetPos(x=473, y=97, width=14, height=14),
        "inky-left-1": SpriteSheetPos(x=489, y=97, width=14, height=14),
        "inky-left-2": SpriteSheetPos(x=505, y=97, width=14, height=14),
        "inky-top-1": SpriteSheetPos(x=521, y=97, width=14, height=14),
        "inky-top-2": SpriteSheetPos(x=537, y=97, width=14, height=14),
        "inky-bottom-1": SpriteSheetPos(x=553, y=97, width=14, height=14),
        "inky-bottom-2": SpriteSheetPos(x=569, y=97, width=14, height=14),

        "clyde-right-1": SpriteSheetPos(x=457, y=113, width=14, height=14),
        "clyde-right-2": SpriteSheetPos(x=473, y=113, width=14, height=14),
        "clyde-left-1": SpriteSheetPos(x=489, y=113, width=14, height=14),
        "clyde-left-2": SpriteSheetPos(x=505, y=113, width=14, height=14),
        "clyde-top-1": SpriteSheetPos(x=521, y=113, width=14, height=14),
        "clyde-top-2": SpriteSheetPos(x=537, y=113, width=14, height=14),
        "clyde-bottom-1": SpriteSheetPos(x=553, y=113, width=14, height=14),
        "clyde-bottom-2": SpriteSheetPos(x=569, y=113, width=14, height=14),

        "blue-ghost-1": SpriteSheetPos(x=584, y=65, width=14, height=14),
        "blue-ghost-2": SpriteSheetPos(x=600, y=65, width=14, height=14),
        "white-ghost-1": SpriteSheetPos(x=616, y=65, width=14, height=14),
        "white-ghost-2": SpriteSheetPos(x=632, y=65, width=14, height=14),

        "ghost-eyes-right": SpriteSheetPos(x=584, y=84, width=9, height=4),
        "ghost-eyes-left": SpriteSheetPos(x=602, y=65, width=9, height=4),
    }

    manager = SpriteService("spritesheet.png", config)
    manager.init_sprites()
