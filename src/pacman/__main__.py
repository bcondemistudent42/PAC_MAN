from pacman.engine.ecs import Position, Velocity, Entity
from pacman.engine.systems.systems import MovementSystem

pacman = Entity("pacman")
pacman.add_component(Position(0, 0))
pacman.add_component(Velocity(1, 0))

mvt_system = MovementSystem()
mvt_system.subscribe(pacman)
mvt_system.run()

# feat docs chore fix refactor 
