import os
from typing import TYPE_CHECKING

import pyray as pr

from pacman.engine.engine import GameEngine
from pacman.engine.scenes.scene import Scene
from pacman.engine.services.sprites import SpriteService
from pacman.game.scenes.components.input import TextInput
from pacman.game.services.score import ScoreEntry, user_list_adapter
from pacman.game.settings import GameSettings

if TYPE_CHECKING:
    from pacman.game.scenes.menu import MenuScene


class EndGameScene(Scene):
    """Shared presentation and score handling for an ended game."""

    TITLE: str
    TITLE_COLOR: pr.Color

    def __init__(
        self,
        settings: GameSettings,
        final_score: int,
        menu_scene: MenuScene,
        sprite_service: SpriteService,
    ):
        """Create an end-game scene.

        Args:
            settings: Window and rendering settings.
            final_score: Score achieved in the completed game.
            menu_scene: Scene returned to after name submission.
            sprite_service: Service used for the chase animation.
        """
        self.settings = settings
        self.final_score = final_score
        self.menu_scene = menu_scene
        self.name = ""

        self.sprite_service = sprite_service

        self.anim_timer = 0.0
        self.anim_index = 0

        self.chasing_right = True
        self.y_pos = self.settings.window_height * 0.75
        self.speed = 350.0

        self.pacman_right_frames = [
            "pacman-right-1",
            "pacman-right-2",
            "pacman-right-3",
            "pacman-right-2",
        ]
        self.pacman_left_frames = [
            "pacman-left-1",
            "pacman-left-2",
            "pacman-left-3",
            "pacman-left-2",
        ]
        self.blinky_right_frames = ["blinky-right-1", "blinky-right-2"]
        self.scared_ghost_frames = ["blue-ghost-1", "blue-ghost-2"]

        input_width = 250
        input_height = 40
        self.name_input = TextInput(
            x=(self.settings.window_width - input_width) // 2,
            y=self.settings.window_height // 2 + 30,
            width=input_width,
            height=input_height,
            max_length=12
        )

    def enter(self, engine: GameEngine) -> None:
        """Reset the chase animation and player name input."""
        self.chasing_right = True
        self.pacman_x = -30.0
        self.ghost_x = -250.0
        self.name_input.text = ""

    def update(self, engine: GameEngine) -> Scene | None:
        """Update animation and return to the menu after name submission."""
        dt = pr.get_frame_time()

        self.name_input.update(dt)

        self.anim_timer += dt
        if self.anim_timer > 0.1:
            self.anim_index += 1
            self.anim_timer = 0.0

        if self.chasing_right:
            self.pacman_x += self.speed * dt
            self.ghost_x += self.speed * dt

            if self.ghost_x > self.settings.window_width + 160:
                self.chasing_right = False
                self.ghost_x = float(self.settings.window_width + 50)
                self.pacman_x = self.ghost_x + 250.0
        else:
            self.pacman_x -= self.speed * dt
            self.ghost_x -= self.speed * dt

            if self.pacman_x < -160:
                self.chasing_right = True
                self.pacman_x = -30.0
                self.ghost_x = -250.0

        if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            clean_name = self.name_input.text.strip()
            if len(clean_name) > 0:
                self.name = clean_name
                return self.menu_scene

        return None

    def render(self, engine: GameEngine) -> None:
        """Draw the final score, name prompt, and chase animation."""
        title = self.TITLE
        title_size = self.settings.window_height // 8
        title_width = pr.measure_text(title, title_size)

        pr.draw_text(
            title,
            (self.settings.window_width - title_width) // 2,
            self.settings.window_height // 6,
            title_size,
            self.TITLE_COLOR,
        )

        score_text = f"SCORE: {self.final_score}"
        score_size = self.settings.window_height // 16
        score_width = pr.measure_text(score_text, score_size)

        pr.draw_text(
            score_text,
            (self.settings.window_width - score_width) // 2,
            self.settings.window_height // 6 + title_size + 20,
            score_size,
            pr.WHITE,
        )

        prompt_text = "ENTER YOUR NAME:"
        prompt_size = 20
        prompt_width = pr.measure_text(prompt_text, prompt_size)
        pr.draw_text(
            prompt_text,
            (self.settings.window_width - prompt_width) // 2,
            self.settings.window_height // 2,
            prompt_size,
            pr.YELLOW
        )
        self.name_input.render()

        footer = "PRESS ENTER TO CONTINUE"
        footer_size = self.settings.window_height // 32
        footer_width = pr.measure_text(footer, footer_size)

        check = int(pr.get_time() * 2) % 2 == 0
        if check and len(self.name_input.text.strip()) > 0:
            pr.draw_text(
                footer,
                (self.settings.window_width - footer_width) // 2,
                self.settings.window_height-(self.settings.window_height // 8),
                footer_size,
                pr.GRAY,
            )

        if self.sprite_service:
            if self.chasing_right:
                pac_frame = self.pacman_right_frames[
                    self.anim_index % len(self.pacman_right_frames)
                ]
                ghost_frame = self.blinky_right_frames[
                    self.anim_index % len(self.blinky_right_frames)
                ]
            else:
                pac_frame = self.pacman_left_frames[
                    self.anim_index % len(self.pacman_left_frames)
                ]
                ghost_frame = self.scared_ghost_frames[
                    self.anim_index % len(self.scared_ghost_frames)
                ]

            pacman_sprite = self.sprite_service.get_sprite(pac_frame)
            ghost_sprite = self.sprite_service.get_sprite(ghost_frame)

            scale = 10

            pr.draw_texture_ex(
                pacman_sprite,
                pr.Vector2(self.pacman_x, self.y_pos),
                0.0,
                scale,
                pr.WHITE,
            )

            pr.draw_texture_ex(
                ghost_sprite,
                pr.Vector2(self.ghost_x, self.y_pos),
                0.0,
                scale,
                pr.WHITE,
            )

    def exit(self, engine: GameEngine) -> None:
        """Persist the submitted score in the leaderboard file."""
        scores = []
        file_path = "storage/scores.json"

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if os.path.exists(file_path):
            with open(file_path, "r") as score_file:
                raw_data = score_file.read()
                if raw_data.strip():
                    scores = user_list_adapter.validate_json(raw_data)

        scores.append(ScoreEntry(
            pseudo=self.name,
            score=self.final_score
        ))

        scores = sorted(scores, key=lambda s: s.score, reverse=True)

        with open(file_path, "wb") as score_file:
            json_bytes = user_list_adapter.dump_json(scores, indent=4)
            score_file.write(json_bytes)
