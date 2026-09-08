from pacman.engine.ecs import Map
from pacman.engine.game_engine import GameEngine
from pacman.engine.ecs import Entity, Map, Position, Sprite, Velocity
from pacman.engine.systems.systems import MovementSystem, SpriteSystem
from pacman.services.sprites import SpriteService, config


def main():
    with GameEngine("world") as world:
        sprite_service = SpriteService("sprites/spritesheet.png", config)
        sprite_service.init_sprites()
        sprite_system = SpriteSystem({SpriteService: sprite_service})
        movement_system = MovementSystem(None)


        p = Position(10, 10)
        v = Velocity(2, 0)
        spr = Sprite("pacman-right-1")

        pac_man = Entity("pac_man")
        pac_man.add_component(p)
        pac_man.add_component(v)
        pac_man.add_component(spr)

        p = Position(10, 30)
        v = Velocity(4, 0)
        spr = Sprite("inky-right-1")
        inky = Entity("inky")
        inky.add_component(p)
        inky.add_component(v)
        inky.add_component(spr)

        p = Position(100, 50)
        v = Velocity(10, 0)

        clyde = Entity("clyde")
        spr = Sprite("clyde-right-1")

        clyde.add_component(p)
        clyde.add_component(v)
        clyde.add_component(spr)

        sprite_system.subscribe(pac_man)
        movement_system.subscribe(pac_man)
        sprite_system.subscribe(clyde)
        movement_system.subscribe(clyde)
        sprite_system.subscribe(inky)
        movement_system.subscribe(inky)

        world.add_system(sprite_system)
        world.add_system(movement_system)

        world.add_entities(pac_man)

        print("testing")
        world.run()
        # print(world.entities[2].components[Map].map)
    print("After")

    # feat docs chore fix refactor 

if __name__ == "__main__":
    # try:
        main()
    # except Exception as e:
        # print(f"\n[ERROR]: {e}\n")