from pacman.engine.game_engine import GameEngine


def main():
    with GameEngine("world") as world:
        world.run()

if __name__ == "__main__":
    # try:
        main()
    # except Exception as e:
        # print(f"\n[ERROR]: {e}\n")


    # feat docs chore fix refactor 