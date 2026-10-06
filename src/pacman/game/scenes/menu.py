from enum import Enum
import sys

from pacman.engine.engine import GameEngine
from pacman.engine.scenes.scene import Scene
from pacman.game.scenes.game import GameScene
from pacman.game.settings import GameSettings
import pyray as pr


class MenuChoice(Enum):
    SCORES = "SCORES"
    PLAY = "PLAYS"
    QUIT = "QUIT"


class MenuScene(Scene):
    def __init__(
        self,
        settings: GameSettings
    ):
        self.settings = settings
        self.choices = ["SCORES", "PLAY", "QUIT"]
        self.status = MenuChoice.PLAY
        self.texture = None

        self.toggle_right = {
            MenuChoice.SCORES: MenuChoice.PLAY,
            MenuChoice.PLAY: MenuChoice.QUIT,
            MenuChoice.QUIT: MenuChoice.SCORES
        }
        self.toggle_left = {
            MenuChoice.SCORES: MenuChoice.QUIT,
            MenuChoice.QUIT: MenuChoice.PLAY,
            MenuChoice.PLAY: MenuChoice.SCORES,
        }

    def enter(self):
        img = pr.load_image("sprites/logo.png")
        pr.image_resize(
            img,
            self.settings.window_width // 2,
            self.settings.window_height // 4
        )
        self.texture = pr.load_texture_from_image(img)

    def update(self) -> Scene | None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_LEFT):
            self.status = self.toggle_left[self.status]
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_RIGHT):
            self.status = self.toggle_right[self.status]
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            if self.status == MenuChoice.PLAY:
                return GameScene(self.settings)
            elif self.status == MenuChoice.QUIT:
                self.exit()
                sys.exit(0)
            else:
                print("Not implemented yet")

    def render(self, engine: GameEngine) -> None:
        if not self.texture:
            return

        choices_colors = {
            MenuChoice.SCORES: pr.WHITE,
            MenuChoice.PLAY: pr.WHITE,
            MenuChoice.QUIT: pr.WHITE
        }

        choices_colors[self.status] = pr.YELLOW

        pr.draw_texture(
            self.texture,
            self.settings.window_width // 4,
            self.settings.window_height // 4,
            pr.WHITE
        )

        mult = 1
        for key, color in choices_colors.items():
            pr.draw_text(
                key.value,
                (self.settings.window_width // 6) * mult,
                (self.settings.window_height // 8) * 4,
                (self.settings.window_height // 16),
                color
            )
            mult *= 2


    def exit(self):
        if self.texture:
            pr.unload_texture(self.texture)
