from pyray import *

class 


def ft_draw_line_h(y: int, x_start: int, x_end: int, color: Pyray.color):
    for x in range(max(x_end - x_start, 0)):
        draw_pixel(x, y, color)

def ft_draw_line_v(x: int, y_start: int, y_end: int, color: Pyray.color):
    for y in range(max(y_end - y_start, 0)):
        draw_pixel(x, y, color)

def init_railyb():

    init_window(800, 450 , "PAC_MAN")

    my_monitor = get_current_monitor()
    monitor_h = int(get_monitor_height(my_monitor) / 4) * 3
    monitor_w = int(get_monitor_width(my_monitor) / 4) * 3

    set_window_size(monitor_w, monitor_h)

    set_target_fps(60)

    while not window_should_close():

        begin_drawing()
        clear_background(BLACK)
        end_drawing()

    close_window()

init_railyb()