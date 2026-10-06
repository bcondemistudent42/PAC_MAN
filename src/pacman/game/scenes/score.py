from typing import TYPE_CHECKING

from pydantic import BaseModel, RootModel, TypeAdapter
import pyray as pr

from pacman.engine.engine import GameEngine
from pacman.engine.scenes.scene import Scene
from pacman.game.settings import GameSettings

if TYPE_CHECKING:
    from pacman.game.scenes.menu import MenuScene


class ScoreEntry(BaseModel):
    pseudo: str
    score: int

user_list_adapter = TypeAdapter(list[ScoreEntry])

class ScoreScene(Scene):
    def __init__(self, settings: GameSettings, menu: MenuScene):
        self.menu = menu
        self.settings = settings
        self.scores: list[ScoreEntry] = []

    def enter(self):
        try:
            with open("storage/scores.json", "r") as f:
                raw_data = f.read()
                self.scores = user_list_adapter.validate_json(raw_data)
        except (FileNotFoundError, ValueError):
            self.scores = []

    def update(self) -> Scene | None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            return self.menu
        return None

    def render(self, engine: GameEngine) -> None:
        title = "LEADERBOARD"
        title_size = self.settings.window_height // 10
        title_width = pr.measure_text(title, title_size)
        pr.draw_text(
            title,
            (self.settings.window_width - title_width) // 2,
            self.settings.window_height // 8,
            title_size,
            pr.YELLOW
        )

        font_size = self.settings.window_height // 16
        start_y = self.settings.window_height // 3
        spacing_y = int(font_size * 1.5)
        center_x = self.settings.window_width // 2

        if not self.scores:
            msg = "AUCUN SCORE"
            msg_width = pr.measure_text(msg, font_size)
            pr.draw_text(msg, center_x - msg_width // 2, start_y, font_size, pr.GRAY)
        else:
            for index, entry in enumerate(self.scores):
                y_pos = start_y + (index * spacing_y)

                pseudo_width = pr.measure_text(entry.pseudo, font_size)
                pr.draw_text(
                    entry.pseudo,
                    center_x - pseudo_width - 30,
                    y_pos,
                    font_size,
                    pr.WHITE
                )

                pr.draw_text(
                    str(entry.score),
                    center_x + 30,
                    y_pos,
                    font_size,
                    pr.YELLOW
                )

        footer = "PRESS ENTER"
        footer_size = self.settings.window_height // 32
        footer_width = pr.measure_text(footer, footer_size)
        pr.draw_text(
            footer,
            (self.settings.window_width - footer_width) // 2,
            self.settings.window_height - (self.settings.window_height // 8),
            footer_size,
            pr.GRAY
        )

    def exit(self):
        pass
