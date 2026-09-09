import pyray as pr
import math

class FtPyray:
    def __init__(self):
        pass

    def start_game(self):
        pr.init_window(800, 450 , "PACMAN")

        my_monitor = pr.get_current_monitor()
        monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
        monitor_h = int(pr.get_monitor_height(my_monitor) / 4) * 3

        pr.set_window_size(monitor_w, monitor_h)
        pr.set_target_fps(60)

        rect_in_w = (monitor_w * 3) // 4
        rect_in_h = (monitor_h * 3) // 4
        x_in = (monitor_w - rect_in_w) // 2
        y_in = (monitor_h - rect_in_h) // 2

        margin = 10
        radius = 20

        rect_out_w = rect_in_w + (margin * 2)
        rect_out_h = rect_in_h + (margin * 2)
        x_out = x_in - margin
        y_out = y_in - margin

        while not pr.window_should_close():
            pr.begin_drawing()

            # self.ft_draw_rectangle((x_in, y_in), rect_in_w, rect_in_h, pr.BLUE)
            # self.ft_draw_rectangle((x_out, y_out), rect_out_w, rect_out_h, pr.BLUE)

            pr.clear_background(pr.BLACK)
            self.ft_draw_rounded_rectangle(
                (x_in, y_in), rect_in_w, rect_in_h, radius, pr.BLUE
            )
            self.ft_draw_rounded_rectangle(
                (x_out, y_out), rect_out_w, rect_out_h, radius, pr.BLUE
            )
            pr.end_drawing()

        pr.close_window()

    def ft_draw_line_h(self, y: int, x_start: int, x_end: int, color: pr.color):
        for x in range(max(x_end - x_start, 0)):
            pr.draw_pixel(x + x_start, y, color)

    def ft_draw_line_v(self, x: int, y_start: int, y_end: int, color: pr.color):
        for y in range(max(y_end - y_start, 0)):
            pr.draw_pixel(x, y + y_start, color)

    def ft_draw_rectangle(
        self,
        start_coord: tuple(int, int),
        length_h : int,
        length_v: int,
        color: pr.color
    ):
        x_start, y_start = start_coord

        self.ft_draw_line_h(y_start, x_start, x_start + length_h, color)
        self.ft_draw_line_v(x_start, y_start, y_start + length_v, color)
        self.ft_draw_line_h(y_start + length_v, x_start, x_start + length_h, color)
        self.ft_draw_line_v(x_start + length_h, y_start, y_start + length_v, color)

# to see how the code works just testing now
    def ft_draw_arc(
        self,
        center_x: int,
        center_y: int,
        radius: int,
        start_angle_deg: float,
        end_angle_deg: float,
        color: pr.Color,
    ):
        start_rad = math.radians(start_angle_deg)
        end_rad = math.radians(end_angle_deg)

        steps = max(int(radius * 2), 16)

        for i in range(steps + 1):
            angle = start_rad + (end_rad - start_rad) * (i / steps)
            x = round(center_x + radius * math.cos(angle))
            y = round(center_y + radius * math.sin(angle))
            pr.draw_pixel(x, y, color)

    def ft_draw_rounded_rectangle(
        self,
        start_coord: tuple[int, int],
        length_h: int,
        length_v: int,
        radius: int,
        color: pr.Color,
    ):
        x, y = start_coord

        self.ft_draw_line_h(
            y, x + radius, x + length_h - radius, color
        )
        self.ft_draw_line_h(
            y + length_v, x + radius, x + length_h - radius, color
        )
        self.ft_draw_line_v(
            x, y + radius, y + length_v - radius, color
        )
        self.ft_draw_line_v(
            x + length_h, y + radius, y + length_v - radius, color
        )

        self.ft_draw_arc(
            x + radius, y + radius, radius, 180, 270, color
        )
        self.ft_draw_arc(
            x + length_h - radius, y + radius, radius, 270, 360, color
        )
        self.ft_draw_arc(
            x + length_h - radius, y + length_v - radius, radius, 0, 90, color
        )
        self.ft_draw_arc(
            x + radius, y + length_v - radius, radius, 90, 180, color
        )
t = FtPyray()
t.start_game()