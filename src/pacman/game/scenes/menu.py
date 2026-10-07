import io
import sys
from enum import Enum

import pyray as pr
from PIL import Image

from pacman.engine.engine import GameEngine
from pacman.engine.scenes.scene import Scene
from pacman.game.scenes.game import GameScene
from pacman.game.scenes.score import ScoreScene
from pacman.game.settings import GameSettings


class MenuChoice(Enum):
    SCORES = "SCORES"
    PLAY = "PLAY"
    QUIT = "QUIT"


class MenuState(Enum):
    SELECTING = "SELECTING"
    EXPLODING = "EXPLODING"


class MenuScene(Scene):
    def __init__(
        self,
        settings: GameSettings
    ):
        self.settings = settings
        self.choices = ["SCORES", "PLAY", "QUIT"]
        self.status = MenuChoice.PLAY
        self.texture = None

        self.toggle_down = {
            MenuChoice.SCORES: MenuChoice.PLAY,
            MenuChoice.PLAY: MenuChoice.QUIT,
            MenuChoice.QUIT: MenuChoice.SCORES
        }
        self.toggle_up = {
            MenuChoice.SCORES: MenuChoice.QUIT,
            MenuChoice.QUIT: MenuChoice.PLAY,
            MenuChoice.PLAY: MenuChoice.SCORES,
        }

        self.state = MenuState.SELECTING
        self.anim_index = 0
        self.anim_timer = 0.0

        self.idle_frames = ["pacman-right-1", "pacman-right-2", "pacman-right-3", "pacman-right-2"]
        self.dead_frames = [f"pacman-dead-{i}" for i in range(1, 12)]

    def enter(self):
        pil_img = Image.open("sprites/logo.png").convert("RGBA")

        target_width = self.settings.window_width // 2
        ratio = pil_img.height / float(pil_img.width)
        target_height = int(target_width * ratio)

        pil_img = pil_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        bytes_arr = io.BytesIO()
        pil_img.save(bytes_arr, format="PNG")
        raw_img = bytes_arr.getvalue()

        img = pr.load_image_from_memory(".png", raw_img, len(raw_img))
        self.texture = pr.load_texture_from_image(img)
        pr.unload_image(img)

        pr.set_texture_filter(self.texture, pr.TextureFilter.TEXTURE_FILTER_BILINEAR)

    def update(self) -> Scene | None:
        self.anim_timer += pr.get_frame_time()

        if self.state == MenuState.SELECTING:
            if self.anim_timer > 0.1:
                self.anim_index = (self.anim_index + 1) % len(self.idle_frames)
                self.anim_timer = 0.0

            if pr.is_key_pressed(pr.KeyboardKey.KEY_UP):
                self.status = self.toggle_up[self.status]
            elif pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN):
                self.status = self.toggle_down[self.status]
            elif pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
                self.state = MenuState.EXPLODING
                self.anim_index = 0
                self.anim_timer = 0.0

        elif self.state == MenuState.EXPLODING:
            if self.anim_timer > 0.04:
                self.anim_index += 1
                self.anim_timer = 0.0

                if self.anim_index >= len(self.dead_frames):
                    if self.status == MenuChoice.PLAY:
                        return GameScene(self.settings)
                    elif self.status == MenuChoice.QUIT:
                        self.exit()
                        sys.exit(0)
                    else:
                        self.state = MenuState.SELECTING
                        self.anim_index = 0
                        self.anim_timer = 0.0
                        return ScoreScene(self.settings, self)

        return None

    def render(self, engine: GameEngine) -> None:
        if not self.texture:
            return

        choices_colors = {
            MenuChoice.SCORES: pr.WHITE,
            MenuChoice.PLAY: pr.WHITE,
            MenuChoice.QUIT: pr.WHITE
        }

        choices_colors[self.status] = pr.YELLOW

        logo_x = (self.settings.window_width - self.texture.width) // 2
        logo_y = int(self.settings.window_height * 0.10)

        pr.draw_texture(
            self.texture,
            logo_x,
            logo_y,
            pr.WHITE
        )

        font_size = self.settings.window_height // 16
        start_y = self.settings.window_height // 2
        spacing_y = int(font_size * 1.5)

        for index, (key, color) in enumerate(choices_colors.items()):
            text_width = pr.measure_text(key.value, font_size)

            final_x = (self.settings.window_width - text_width) // 2
            final_y = start_y + (index * spacing_y)

            if key == self.status and hasattr(self, 'sprite_service'):
                if self.state == MenuState.SELECTING:
                    sprite_name = self.idle_frames[self.anim_index]
                else:
                    safe_index = min(self.anim_index, len(self.dead_frames) - 1)
                    sprite_name = self.dead_frames[safe_index]

                pacman_sprite = self.sprite_service.get_sprite(sprite_name)
                pacman_scale = font_size / pacman_sprite.height
                pac_x = final_x - (pacman_sprite.width * pacman_scale) - 20

                pr.draw_texture_ex(
                    pacman_sprite,
                    pr.Vector2(pac_x, final_y),
                    0.0,
                    pacman_scale,
                    pr.WHITE
                )

            pr.draw_text(
                key.value,
                int(final_x),
                int(final_y),
                font_size,
                color
            )

    def exit(self):
        if self.texture:
            pr.unload_texture(self.texture)
