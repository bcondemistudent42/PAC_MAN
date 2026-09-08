from pacman.engine.ecs import Entity, Position, Sprite, Velocity
from pacman.engine.systems.systems import MovementSystem, SpriteSystem

def main():

    pacman = Entity("pacman")
    pacman.add_component(Position(0, 0))
    pacman.add_component(Velocity(1, 0))
    pacman.add_component(Sprite("sprites/ghost_sprites/blue/blue_right.png"))

    mvt_system = MovementSystem()
    mvt_system.subscribe(pacman)
    mvt_system.run() 

    import pyray as pr

    sp_sys = SpriteSystem()
    sp_sys.subscribe(pacman)

    pr.init_window(800, 450 , "PACMAN")
    my_monitor = pr.get_current_monitor()
    monitor_w = int(pr.get_monitor_width(my_monitor) / 4) * 3
    monitor_h = int(pr.get_monitor_height(my_monitor) / 4) * 3
    pr.set_window_size(monitor_w, monitor_h)
    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        sp_sys.run()
        mvt_system.run()
        pacman.add_component(Velocity(1, 0))
        pr.end_drawing()
    pr.close_window()

    # feat docs chore fix refactor 

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR]: {e}\n")