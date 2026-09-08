from pacman.engine.ecs import Map
from pacman.engine.game_engine import GameEngine


def main():


    with GameEngine("world") as world:
        print("testing")
        # print(world.entities)
        print(world.entities[2].components[Map].map)
    print("After")

    # feat docs chore fix refactor 

if __name__ == "__main__":
    # try:
        main()
    # except Exception as e:
        # print(f"\n[ERROR]: {e}\n")