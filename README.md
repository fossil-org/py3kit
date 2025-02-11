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

## Roadmap:

### 20.12.2024
- development of py3kit has begun

### 25.1.2025
- first public release
- created GitHub repository
- initial commit in the GitHub repository

### 8.2.2025
- added `OutOfBounds` checks and `ShapeCollision` checks for shapes and tags moved using pistons
- - piston `ShapeCollision` checks rely on `game.after` (checks every game loop). This means `ShapeCollision` checks only work if the shape/tag being pushed doesn't move faster than the game loop speed (this is basically impossible anyway)
- added **2 new bots**:
- - `ReverseBot` in `game/bots/reverse` - Walks away from a location at all costs, basically the opposite of `SimpleBot` in `game/bots/simple`, hence the name `ReverseBot`.
- - `AvoidBot` in `game/bots/avoid` - Avoids a tag at all costs, basically the opposite of `FollowerBot` in `game/bots/follower`, hence the name `AvoidBot`.
- updated the README
- reworked how bots move (not noticeable while playing, but the new method is much more flexible in practice)
- bug fixes

## 9.2.2025
- fixed some bugs with pistons
- reworked parameters of the `Player` class from `game/player`
- - old: `Player(icon, location, speed, states_tm)`
- - new: `Player(piston, speed, icon, location, opo, states_tm)`
- - the `opo` (`OnPlayerOverwrite`) parameter is optional, default: `OnPlayerOverwrite.ERROR`
- `Player` class from `game/player` location parameter is now optional (uses autofill, requires states_tm parameter)
- `game.player` now has an attribute `game`, which points to the game the player is in.
- `Piston` class from `game/piston` game parameter is now optional, but it has to be specified later for the piston to work.
- `ReverseBot` from `game/bots/reverse` and `AvoidBot` from `game/bots/avoid` now have working `on_arrived` callbacks.
- big rework to player movement, `game` no longer handles player movement and only provides the query to `game.piston`
- the player is now a tile (NOT a `Tile` shape)
- MANY bug fixes
- added death (`game.player.on_death`)
- - triggered when the player is not found on the board (for ex. overwritten/crushed by a tile or shape)
- player services can be provided to `game` (`Game(player, *boards, **player_services)`)

# 11.2.2025
- finally, fixed a bug where moving the player an number of spaces that is less than the player's speed would bug out and create a copy.
- QoL changes
- `tm.apply_offset` removed
- `tm.move_tag` added
- changed `piston.push`
- fixed distance in pistons