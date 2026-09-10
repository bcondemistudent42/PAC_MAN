import pyray as pr
from pacman.engine.ecs import Map
from pacman.engine.game_engine import GameEngine

pr.set_trace_log_level(pr.LOG_NONE)

def main():
    with GameEngine("world") as world:
        # print(world.entities[0].components[Map].map)
        world.run()

if __name__ == "__main__":
    # try:
        main()
    # except Exception as e:
        # print(f"\n[ERROR]: {e}\n")


    # feat docs chore fix refactor 
    # to scale all the images