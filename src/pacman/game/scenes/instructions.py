import random
from typing import TYPE_CHECKING

import pyray as pr

from pacman.engine.engine import GameEngine
from pacman.engine.scenes.scene import Scene
from pacman.game.settings import GameSettings

if TYPE_CHECKING:
    from pacman.game.scenes.menu import MenuScene


class InstructionsScene(Scene):
    """Display the controls and objective of the game."""

    def __init__(self, settings: GameSettings, menu: MenuScene):
        """Create the instructions screen.

        Args:
            settings: Window and rendering settings.
            menu: Scene returned to when the player presses Enter.
        """
        self.settings = settings
        self.menu = menu
        self.instructions = [
            ("ARROW KEYS", "Move Pac-Man"),
            ("PAC-DOTS", "Collect them all to clear the maze"),
            ("POWER PELLETS", "Eat ghosts while they are scared"),
            ("SPACE", "Pause or resume the game"),
            ("BACKSPACE", "Return to the main menu"),
            ("CTRL / C / S", "Show cheats / trap / scare ghosts"),
        ]

    def enter(self, engine: GameEngine) -> None:
        """Prepare the animated background."""
        self.stars = [
            (
                random.randint(0, self.settings.window_width),
                random.randint(0, self.settings.window_height),
                random.choice([2, 2.5, 3]),
            )
            for _ in range(200)
        ]

    def update(self, engine: GameEngine) -> Scene | None:
        """Return to the menu when the player presses Enter."""
        if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            return self.menu
        return None

    def render(self, engine: GameEngine) -> None:
        """Draw the controls, objective, and animated background."""
        for x, y, radius in self.stars:
            pr.draw_circle(
                int(x), int(y), radius, pr.Color(222, 161, 133, 255)
            )

        title = "HOW TO PLAY"
        title_size = self.settings.window_height // 10
        title_width = pr.measure_text(title, title_size)
        pr.draw_text(
            title,
            (self.settings.window_width - title_width) // 2,
            self.settings.window_height // 8,
            title_size,
            pr.YELLOW,
        )

        font_size = self.settings.window_height // 32
        line_spacing = int(font_size * 2.2)
        start_y = self.settings.window_height // 3
        center_x = self.settings.window_width // 2

        for index, (control, description) in enumerate(self.instructions):
            y = start_y + index * line_spacing
            control_width = pr.measure_text(control, font_size)
            description_width = pr.measure_text(description, font_size)
            gap = font_size
            row_width = control_width + gap + description_width
            row_x = center_x - row_width // 2

            pr.draw_text(control, row_x, y, font_size, pr.YELLOW)
            pr.draw_text(
                description,
                row_x + control_width + gap,
                y,
                font_size,
                pr.WHITE,
            )

        footer = "PRESS ENTER TO RETURN"
        footer_size = self.settings.window_height // 32
        footer_width = pr.measure_text(footer, footer_size)
        if int(pr.get_time() * 2) % 2 == 0:
            pr.draw_text(
                footer,
                (self.settings.window_width - footer_width) // 2,
                self.settings.window_height
                - (self.settings.window_height // 8),
                footer_size,
                pr.GRAY,
            )

    def exit(self, engine: GameEngine) -> None:
        """Release scene resources."""
        pass
