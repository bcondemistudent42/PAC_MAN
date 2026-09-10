import pyray as pr
from pacman.services.sprites import config, SpriteService

import pyray as pr
import math

class FtPyray:
    def __init__(self):
        pass

    def start_game(self):
        pr.init_window(800, 450 , "PACMAN")

        my_monitor = pr.get_current_monitor()
        monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
        monitor_h = int(pr.get_monitor_height(my_monitor) / 10) * 8

        pr.set_window_size(monitor_w, monitor_h)

        rect_in_w = (monitor_w * 6) // 10
        rect_in_h =( monitor_h * 9) // 10
        x_in = (monitor_w - rect_in_w) // 2
        y_in = (monitor_h - rect_in_h) // 2

        margin = 10
        radius = 20

        rect_out_w = rect_in_w + (margin * 2)
        rect_out_h = rect_in_h + (margin * 2)
        x_out = x_in - margin
        y_out = y_in - margin

# to put the actual last sprite of the entities in a list and then extend it 
# with the death sprites to follow animiation
        img_to_display = [
            "pacman-dead-1",
            "pacman-dead-2",
            "pacman-dead-3",
            "pacman-dead-4",
            "pacman-dead-5",
            "pacman-dead-6",
            "pacman-dead-7",
            "pacman-dead-8",
            "pacman-dead-9",
            "pacman-dead-10",
            "pacman-dead-11"
            ]

        manager = SpriteService("sprites/spritesheet.png", config)
        manager.init_sprites()

        pr.set_target_fps(10)
        i = 0
        while not pr.window_should_close():
            i += 1
            if i >= len(img_to_display):
                i = 0
            pr.begin_drawing()

            pr.clear_background(pr.BLACK)
            
            img = manager.get_sprite(img_to_display[i])
            pr.clear_background(pr.BLACK)
            pr.draw_texture(img, 10, 10, pr.WHITE)
            pr.clear_background(pr.BLACK)


            # self.ft_draw_rounded_rectangle(
            #     (x_in, y_in), rect_in_w, rect_in_h, radius, pr.BLUE
            # )
            # self.ft_draw_rounded_rectangle(
            #     (x_out, y_out), rect_out_w, rect_out_h, radius, pr.BLUE
            # )

            pr.end_drawing()

        pr.close_window()

t = FtPyray()
t.start_game()
print("SUCESS")
