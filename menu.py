import pyray as pr


def menu():


    pr.init_window(800, 600, "Afficher une image avec pyray")

    my_monitor = pr.get_current_monitor()
    monitor_w = int(pr.get_monitor_width(my_monitor) * 0.75)
    monitor_h = int(pr.get_monitor_height(my_monitor) * 0.75)

    pr.set_window_size(monitor_w, monitor_h)

    img = pr.load_image("sprites/logo.png")
    pr.image_resize(img, monitor_w // 2, monitor_h // 4)
    texture = pr.load_texture_from_image(img)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pr.draw_texture(texture, monitor_w // 4, monitor_h // 4, pr.WHITE)
        pr.draw_text("SCORES", monitor_w // 6, (monitor_h // 8) * 4, (monitor_h // 16), pr.WHITE)
        pr.draw_text("PLAY", ((monitor_w // 6) * 2) + (monitor_w // 8), (monitor_h // 8) * 4, (monitor_h // 16), pr.WHITE)
        pr.draw_text("QUIT", ((monitor_w // 6) * 4) + (monitor_w // 16), (monitor_h // 8) * 4, (monitor_h // 16), pr.WHITE)
        pr.end_drawing()

    pr.close_window()


menu()