import pyray as pr
import raylib as rb

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
        
        img = pr.load_texture("manpac.png")
        # testing to see sprite functionnement

        while not pr.window_should_close():
            pr.begin_drawing()
            # self.ft_draw_rectangle((50,50), 100, 500, pr.WHITE)
            pr.clear_background(pr.BLACK)
            pr.draw_texture(img, 10, 10, pr.WHITE)
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

t = FtPyray()
t.start_game()