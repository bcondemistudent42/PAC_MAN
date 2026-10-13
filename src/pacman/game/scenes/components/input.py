import pyray as pr

class TextInput:
    def __init__(self, x: int, y: int, width: int, height: int, max_length: int = 15):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_length = max_length
        self.font_size = 20

        self.text = ""

        self.cursor_visible = True
        self.cursor_timer = 0.0
        self.blink_rate = 0.5

    def update(self, dt: float):
        char_pressed = pr.get_char_pressed()

        while char_pressed > 0:
            if 32 <= char_pressed <= 125 and len(self.text) < self.max_length:
                self.text += chr(char_pressed)

            char_pressed = pr.get_char_pressed()

        if pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE):
            self.text = self.text[:-1]

        self.cursor_timer += dt
        if self.cursor_timer >= self.blink_rate:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0.0

    def render(self):
        pr.draw_rectangle(self.x, self.y, self.width, self.height, pr.BLACK)
        pr.draw_rectangle_lines(self.x, self.y, self.width, self.height, pr.WHITE)

        text_x = self.x + 10
        text_y = self.y + (self.height - self.font_size) // 2

        pr.draw_text(self.text, text_x, text_y, self.font_size, pr.WHITE)

        if self.cursor_visible:
            text_width = pr.measure_text(self.text, self.font_size)
            cursor_x = text_x + text_width + 2
            pr.draw_rectangle(cursor_x, text_y, 10, self.font_size, pr.WHITE)
