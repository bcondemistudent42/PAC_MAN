# Project Management & Methodology Report

This document outlines the project management approach, team organization, technical analysis, and quality assurance processes followed during the development of the Pac-Man ECS Engine project.

---

## 1. Team Organization & Workflow

### Roles and Responsibilities
To ensure smooth development and avoid overlapping work, the project was divided into distinct ownership areas:
*   **abounoua**: Core Engine Architecture (ECS), Scene Management, Game Loop, and Collision System, Sprite Management (`SpriteService`), UI/HUD, Highscore system (JSON/Pydantic) and Procedural Maze Generation.
*   **bcondemi**: Parsing (JSON/Pydantic), UI/HUD Ghost Artificial Intelligence (A* Pathfinding, Behaviors, State machine), Game factories, Sprites animation and score/time handling.


### Decision-Making Process
*   **Daily Syncs**: 15-minute daily stand-up meetings on Discord to discuss progress, blockers, and the day's objectives.
*   **Architecture Validation**: Major architectural decisions (such as using an ECS over standard OOP) were discussed and agreed upon unanimously before implementation.

### Version Control (Git Workflow)
We adopted a simplified **Feature Branch Workflow**:
*   `main`: Stable, production-ready code.
*   Feature branches: Named explicitly (e.g., `feature/ecs-core`, `fix/ghost-collision`, `feature/a-star`).
*   **Pull Requests (PRs)**: No direct pushes to `main`. Every PR required a code review from at least one other team member to prevent merge conflicts and ensure code quality.
*   **Precommit**: No direct pushes without strict linting and typing using Ruff precommit hooks.

---

## 2. Project Timeline & Progress Tracking

We managed our tasks using a basic tracking sheet, moving tickets through `Backlog`, `To Do`, `In Progress`, and `Done`.

### Planned Timeline vs. Actual Progress

| Phase | Planned Duration | Focus | Actual Progress / Delays |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Week 1 | Core ECS Engine setup, Pyray window init, basic entity rendering. | **On time.** The ECS abstraction was set up quickly. |
| **Phase 2** | Week 2 | Maze generation (perfect maze -> broken walls), Pac-Man movement, basic collisions. | **Slight delay (+2 days).** Tweaking the `generate_matrix` and `break_dead_ends` algorithms to make the maze feel like an authentic Pac-Man map using tile mapping took longer than expected. |
| **Phase 3** | Week 3 | Ghost AI (Blinky, Pinky, Inky, Clyde), A* pathfinding, pellet consumption. Abstraction leaks| **On time.** Implementing Inky's vector-based targeting required intense debugging, but was completed within the week. |
| **Phase 4** | Week 4 | Game loop polish (Super Pac-Gum states, UI, menus, Highscore, bug fixing). | **On time.** Pydantic integration for the leaderboard saved time on data validation. |

---

## 3. Project Analysis & Technical Choices

*   **Custom ECS over OOP**: Pac-Man requires many interacting entities. A deep OOP inheritance tree (e.g., `MovingEntity -> Ghost -> Blinky`) would have become rigid. The ECS pattern allowed us to compose entities purely from data (e.g., a Ghost is just a `Position` + `Velocity` + `Sprite` + `Target`), making the collision and rendering systems completely decoupled and reusable.
*   **Maze Generation Approach**: The `mazegenerator` package creates perfect mazes (no loops). Pac-Man requires loops to outmaneuver ghosts. We implemented a custom bitwise algorithm (`break_dead_ends`) that traverses the perfect maze and randomly breaks specific walls while preserving grid integrity, creating a highly playable map.
*   **Pathfinding**: We implemented a custom A* (`Astar`) algorithm using Python's `heapq` and Manhattan distance heuristics. To save CPU cycles, pathfinding is only recalculated at maze intersections rather than every frame.

---

## 4. Risk Analysis & Mitigation

| Identified Risk | Impact | Probability | Mitigation Strategy Applied |
| :--- | :---: | :---: | :--- |
| **Memory Leaks (Textures)** | High | High | Raylib requires manual memory management for textures. We centralized this in a `SpriteService` that loads sprites into a dictionary and explicitly unloads them (`unload_texture`) when the application exits. |
| **Pathfinding Performance Drop**| Medium | Medium | 4 ghosts running A* every frame at 60 FPS would lag Python. We optimized this by restricting A* calculations to grid cell centers and caching targets. |
| **Git Merge Conflicts** | High | High | Strict decoupling. By separating systems (`CollisionSystem`, `MovementSystem`) into their own files, developers rarely edited the same files simultaneously. |

---

## 5. Acceptance Test Plan

Before considering the project "Done", we ran manual acceptance tests to ensure game stability:

1.  **Wall Collision Test**: Move Pac-Man into walls from all 4 directions. *Result: Passed. Pac-Man slides along walls if intentions don't match open paths.*
2.  **Pacgum Consumption**: Eat all pacgum on the map. *Result: Passed. Reaching 0 pacgums triggers the `WinScene` and prompts for highscore.*
3.  **Super Pac-Gum Mechanics**: Eat a power pellet. *Result: Passed. Ghosts turn blue, slow down by 30%, flee to corners, and can be eaten. They respawn correctly at their home base after being eaten.*
4.  **Ghost Personality Test**: Verify that Blinky chases directly, while Pinky tries to cut off Pac-Man. *Result: Passed. Monitored target tiles visually during debug mode.*
5.  **Score Persistence**: Enter a name with special characters/spaces on the game over screen. *Result: Passed. Pydantic parser successfully handles and saves the JSON safely.*

---

## 6. Summary of Blocking Points & Conflict Resolution

### Technical Blockers
*   **System Execution Order**: Initially, ghosts were killing Pac-Man even when they were scared, due to the order in which Systems were executing. 
    *   *Resolution*: We restructured the `GameEngine` loop to ensure the `CollisionSystem` dispatches events, and the `DeathSystem` processes them *before* the `MovementSystem` advances the next frame.
*   **Alpha Channels in Sprite Sheets**: Extracting sprites with PIL and passing them to Raylib resulted in black backgrounds instead of transparency.
    *   *Resolution*: We implemented a numpy mask in `SpriteService` to identify exact black pixels (`[0, 0, 0]`) and set their alpha channel to 0 before saving to memory.
*   **Grid Movement & Snapping**: Entities move continuously using pixel velocities (`float`), but the maze requires strict grid-based 90-degree turns. Overshooting a tile center prevented entities from turning correctly and misaligned them with the logical matrix.
    *   *Resolution*: We introduced a snapping rule in the `MovementSystem`. If an entity's distance to the target cell's center is less than `speed / 2`, its position is explicitly snapped to the exact center coordinates, allowing smooth and flawless directional changes.
*   **Tile Mapping for Map Generation**: Translating the raw bitwise maze data into a visually cohesive map with continuous walls, corners, and junctions was extremely tedious, especially while needing to maintain a parallel logical matrix for collisions.
    *   *Resolution*: We developed a robust tile mapping algorithm (`maze_to_matrix` in `PacmanMap`). It evaluates the bitwise connections (North, South, East, West) of each cell and its neighbors to determine the exact visual sprite (e.g., `corner-jonction-top-left`), while concurrently populating a `logic_matrix` (`PacmanCell.WALL`, `PacmanCell.PACGUM`) for the ECS.
*   **Leaky Abstractions in ECS**: As gameplay complexified, some systems started handling logic outside their intended scope (e.g., movement systems directly reading the Pac-Man specific map matrix), causing a "leaky abstraction" that coupled the generic engine to specific game rules.
    *   *Resolution*: We refactored the architecture to enforce strict boundaries. We abstracted the map reading behind a generic `NavigationService` passed via `Resources`. The engine remains purely agnostic, and systems only communicate through shared components or the decoupled `EventsQueue`.


### Conflict Resolution
Most technical discussions centered around maintaining architectural purity rather than tooling. For instance, if a team member accidentally introduced a leaky abstraction, bypassed strict ECS rules, or tightly coupled rendering with business logic, we didn't simply reject the code. Instead, we treated it as a collaborative learning opportunity. We would sit down together to discuss the architectural implications, helping the team member progress in their understanding of software design, and then collaboratively refactored the code to ensure the engine remained strictly decoupled and clean.