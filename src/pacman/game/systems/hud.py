import pyray as pr

from pacman.engine.systems.system import System
from pacman.game.resources import PacmanResources
from pacman.game.settings import GameSettings


class HUDSystem(System):
    def __init__(
        self, resources: PacmanResources, settings: GameSettings
    ) -> None:
        super().__init__([])
        self.resources = resources
        self.settings = settings

    def run(self) -> None:
        window_height = self.settings.window_height
        hud_x = int(self.settings.window_width * 2 / 3)
        margin = max(16, window_height // 40)
        font_size = max(20, window_height // 24)

        score_y = window_height // 16
        time_y = score_y + font_size + margin
        lives_y = time_y + font_size + margin

        pr.draw_text(
            f"Score: {self.resources.score}",
            hud_x,
            score_y,
            font_size,
            pr.WHITE,
        )
        pr.draw_text(
            f"Time remaining: {self.resources.time_left:.2f}",
            hud_x,
            time_y,
            font_size,
            pr.WHITE,
        )
        pr.draw_text("Lives:", hud_x, lives_y, font_size, pr.WHITE)

        sprite_service = self.resources.sprite_service
        if sprite_service is None:
            return

        life_sprite = sprite_service.get_sprite("pacman-right-2")
        life_spacing = max(
            int(self.resources.scale * 15),
            int(life_sprite.width * self.resources.scale) + margin,
        )
        life_y = lives_y + font_size + margin

        for index in range(self.resources.data_score.lives):
            pr.draw_texture_ex(
                life_sprite,
                pr.Vector2(hud_x + life_spacing * index, life_y),
                0.0,
                self.resources.scale,
                pr.WHITE,
            )