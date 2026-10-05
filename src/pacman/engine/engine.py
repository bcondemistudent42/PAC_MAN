import pyray as pr

from pacman.engine.components import Entity
from pacman.engine.events.queue import EventsQueue
from pacman.engine.systems import System


class GameEngine:
    def __enter__(self):
        pr.init_window(self.window_width, self.window_height, "PACMAN")
        my_monitor = pr.get_current_monitor()
        monitor_w = int(pr.get_monitor_width(my_monitor) * 0.75)
        monitor_h = int(pr.get_monitor_height(my_monitor) * 0.75)
        self.monitor_w = monitor_w
        self.monitor_h = monitor_h
        pr.set_window_size(monitor_w, monitor_h)
        pr.set_target_fps(60)
        img = pr.load_image("sprites/logo.png")
        pr.image_resize(img, monitor_w // 2, monitor_h // 4)
        self.texture = pr.load_texture_from_image(img)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pr.close_window()

    def __init__(self):
        self.entities: list[Entity] = []
        self.systems: list[System] = []
        self.events = EventsQueue()
        self.window_width = 1600
        self.window_height = 1000
        # this is defining also the game size, to check with anselme find it strange

    def add_system(self, system: list[System] | System) -> None:
        if isinstance(system, System):
            self.systems.append(system)
        elif isinstance(system, list):
            self.systems.extend(system)
        else:
            raise TypeError("Cannot add this in system to adapt add system")

    def add_entities(self, entity: Entity | list[Entity]) -> None:
        if isinstance(entity, Entity):
            self.add_single_entity(entity)
        elif isinstance(entity, list):
            for e in entity:
                self.add_single_entity(e)
        else:
            raise TypeError(
                "Cannot add this in entities to adapt add entities")

    def add_single_entity(self, entity: Entity) -> None:
        self.entities.append(entity)

        for system in self.systems:
            if not system.required_components:
                continue
            if all(
                required in entity.components for required in system.required_components
            ):
                system.subscribe(entity)

    def run(self):
        # to refacto first make it work
        index = 1
        choice = "PLAY"
        ready = False
        playing = False

        while not pr.window_should_close():
            pr.begin_drawing()
            pr.clear_background(pr.BLACK)

            if not playing:
                self.display_menu(index)
                if pr.is_key_pressed(pr.KeyboardKey.KEY_LEFT): #left arrow
                    index -= 1
                    choice = self.display_menu(index % 3)
                if pr.is_key_pressed(pr.KeyboardKey.KEY_RIGHT): #right arrow
                    index += 1
                    choice = self.display_menu(index % 3)
                if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
                    if choice == "PLAY":
                        ready = True
                    elif choice == "QUIT":
                        return
                    else:
                        print(choice)
                        print("\n===============")
                        print("Not implemented yet")
                        print("===============\n")
                        exit(1)

            if choice == "PLAY" and ready:
                playing = True
                for system in self.systems:
                    system.run()

            self.events.drain()
            pr.end_drawing()

    def display_menu(self, index: int):
        lst_choices = ["SCORES", "PLAY", "QUIT"]
        choices_colors = {
            "SCORES": pr.WHITE,
            "PLAY": pr.WHITE,
            "QUIT": pr.WHITE
        }

        if index >= len(lst_choices):
            return
        selected = lst_choices[index]
        choices_colors[selected] = pr.YELLOW

        choices_colors[selected] = pr.YELLOW
        pr.draw_texture(self.texture, self.monitor_w // 4, self.monitor_h // 4, pr.WHITE)
        pr.draw_text(lst_choices[0], self.monitor_w // 6, (self.monitor_h // 8) * 4, (self.monitor_h // 16), choices_colors[lst_choices[0]])
        pr.draw_text(lst_choices[1], ((self.monitor_w // 6) * 2) + (self.monitor_w // 8), (self.monitor_h // 8) * 4, (self.monitor_h // 16), choices_colors[lst_choices[1]])
        pr.draw_text(lst_choices[2], ((self.monitor_w // 6) * 4) + (self.monitor_w // 16), (self.monitor_h // 8) * 4, (self.monitor_h // 16), choices_colors[lst_choices[2]])

        return selected