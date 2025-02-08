# py3kit
All the resources you need to make an in-terminal game, bundled up in one lightweight library.

## Game file structure:
```
my_game/
  src/
    main.py
    include
    (add any modules here)
  scripts/
    (add any scripts here)
```

## How to run your game

```
python3 -m py3kit # this will run the game in .
python3 -m py3kit path/to/my/game # this will run the game in path/to/my/game
```

## Patch notes:


### 8.2.2025

- added `OutOfBounds` checks and `ShapeCollision` checks for shapes and tags moved using pistons
- - piston `ShapeCollision` checks rely on `game.after` (checks every game loop). This means `ShapeCollision` checks only work if the shape/tag being pushed doesn't move faster than the game loop speed (this is basically impossible anyway)
- added **2 new bots**:
- - `ReverseBot` in `game/bots/reverse` - Walks away from a location at all costs, basically the opposite of `SimpleBot` in `game/bots/simple`, hence the name `ReverseBot`.
- - `AvoidBot` in `game/bots/avoid` - Avoids a tag at all costs, basically the opposite of `FollowerBot` in `game/bots/follower`, hence the name `AvoidBot`.
- updated the README
- reworked how bots move (not noticeable while playing, but the new method is much more flexible in practice)
- bug fixes