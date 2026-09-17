import math

import pyray as pr

pr.set_trace_log_level(pr.LOG_NONE)


class FtPyray:
    def __init__(self, maze):
        self.maze = maze

    def start_game(self):

        my_monitor = pr.get_current_monitor()
        monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
        monitor_h = int(pr.get_monitor_height(my_monitor) / 10) * 8
        pr.init_window(monitor_w, monitor_h, "PACMAN")

        pr.set_target_fps(60)

        rect_in_w = (monitor_w * 6) // 10
        rect_in_h = (monitor_h * 9) // 10
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
            pr.clear_background(pr.BLACK)

    # multiply cell size of 50 by the index 
            for i, line in enumerate(self.maze):
                for j, cell in enumerate(line):

                    if cell & 1 == 0:
                        FtPyray.draw_wall_horizontal(
                            x_in + (50 * i),
                            y_in + (50 * j)
                        )

                    if cell >> 1 & 1 == 0:
                        FtPyray.draw_wall_vertical(
                            x_in + (50 * i),
                            y_in + (50 * j)
                        )

                    if cell >> 2 & 1 == 0:
                        FtPyray.draw_wall_horizontal(
                            (x_in) + (50 * i),
                            (y_in + 50) + (50 * j)
                        )

                    if cell >> 3 & 1 == 0:
                        FtPyray.draw_wall_vertical(
                        (x_in + 50) + (50 * i),
                        (y_in) + (50 * j)
                    )

            # self.ft_draw_rounded_rectangle(
            #     good_t, rect_in_w, rect_in_h, radius, pr.BLUE
            # )
            # self.ft_draw_rounded_rectangle(
            #     (x_out, y_out), rect_out_w, rect_out_h, radius, pr.BLUE
            # )
            pr.end_drawing()

        pr.close_window()

    @staticmethod
    def ft_draw_line_h(y: int, x_start: int, x_end: int, color: pr.color):
        for x in range(max(x_end - x_start, 0)):
            pr.draw_pixel(x + x_start, y, color)

    @staticmethod
    def ft_draw_line_v(x: int, y_start: int, y_end: int, color: pr.color):
        for y in range(max(y_end - y_start, 0)):
            pr.draw_pixel(x, y + y_start, color)

    @staticmethod
    def ft_draw_rectangle(
        start_coord: tuple(int, int),
        length_h: int,
        length_v: int,
        color: pr.color,
    ):
        x_start, y_start = start_coord

        FtPyray.ft_draw_line_h(y_start, x_start, x_start + length_h, color)
        FtPyray.ft_draw_line_v(x_start, y_start, y_start + length_v, color)
        FtPyray.ft_draw_line_h(y_start + length_v, x_start, x_start + length_h, color)
        FtPyray.ft_draw_line_v(x_start + length_h, y_start, y_start + length_v, color)

    @staticmethod
    def ft_draw_arc(
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

    @staticmethod
    def ft_draw_rounded_rectangle(
        start_coord: tuple[int, int],
        length_h: int,
        length_v: int,
        radius: int,
        color: pr.Color,
    ):
        x, y = start_coord

        FtPyray.ft_draw_line_h(y, x + radius, x + length_h - radius, color)
        FtPyray.ft_draw_line_h(y + length_v, x + radius, x + length_h - radius, color)
        FtPyray.ft_draw_line_v(x, y + radius, y + length_v - radius, color)
        FtPyray.ft_draw_line_v(x + length_h, y + radius, y + length_v - radius, color)

        # top right corner
        FtPyray.ft_draw_arc(x + radius, y + radius, radius, 180, 270, color)
        FtPyray.ft_draw_arc(x + length_h - radius, y + radius, radius, 270, 360, color)
        FtPyray.ft_draw_arc(
            x + length_h - radius, y + length_v - radius, radius, 0, 90, color
        )
        FtPyray.ft_draw_arc(x + radius, y + length_v - radius, radius, 90, 180, color)

    def draw_wall_vertical(x: int, y: int):
        FtPyray.ft_draw_rounded_rectangle(
            (x, y),
            17,
            50,
            10,
            pr.BLUE
        )

    def draw_wall_horizontal(x: int, y: int):
        FtPyray.ft_draw_rounded_rectangle(
            (x, y),
            50,
            17,
            10,
            pr.BLUE
        )


maze = [
    [9, 1, 5, 3, 9, 3, 9, 5, 5, 5, 5, 5, 5, 1, 3],
    [8, 0, 3, 8, 0, 4, 2, 9, 1, 1, 1, 3, 9, 4, 2],
    [10, 8, 4, 4, 2, 9, 2, 12, 0, 2, 8, 2, 12, 5, 2],
    [10, 12, 1, 5, 0, 6, 12, 3, 8, 2, 10, 12, 1, 3, 10],
    [12, 1, 4, 1, 6, 9, 1, 2, 12, 4, 4, 1, 2, 10, 10],
    [9, 2, 9, 6, 15, 10, 8, 2, 15, 15, 15, 10, 10, 8, 2],
    [10, 10, 8, 3, 15, 12, 6, 8, 5, 7, 15, 8, 2, 8, 6],
    [10, 8, 2, 10, 15, 15, 15, 10, 15, 15, 15, 10, 8, 4, 3],
    [10, 8, 4, 2, 9, 3, 15, 10, 15, 13, 5, 2, 12, 5, 2],
    [8, 4, 3, 10, 10, 10, 15, 10, 15, 15, 15, 8, 1, 5, 2],
    [8, 3, 12, 4, 4, 4, 1, 0, 5, 1, 3, 12, 4, 5, 2],
    [8, 6, 9, 5, 1, 5, 2, 8, 1, 2, 10, 9, 5, 3, 10],
    [8, 3, 8, 3, 12, 1, 2, 8, 2, 10, 8, 4, 1, 2, 10],
    [10, 8, 6, 12, 1, 4, 6, 12, 0, 2, 8, 3, 10, 10, 10],
    [12, 4, 5, 5, 4, 5, 5, 5, 6, 12, 4, 6, 12, 4, 6],
]


t = FtPyray(maze)
t.start_game()
