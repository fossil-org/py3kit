class BaseShape:
    STRUCTURE: list[tuple[int, ...]] = [
        # enter a structure here
        # examples:
        # (0, 0) is the bottom left corner
        # (0, 1) is one tile above the bottom left corner
        # (1, 0) is one tile to the right of the bottom left corner
    ]
    def __init__(self, material, name: str | None = None, destruction = None):
        from random import randint
        self.name: str = name or f"{self.__class__.__name__}N{str(randint(1, 999))}"
        from ...render.icon import Icon
        if not isinstance(material, Icon):
            raise TypeError("Material must be an instance of Icon")
        self.material: Icon = material
        self.loc: list[tuple[int, ...]] = []
        self.live_locations: list[tuple[int,...]] = []
        self.placed: bool = False
        self.destroyed: bool = False
        from ..destruction import Destruction
        self.destruction: Destruction = destruction or Destruction.SOLID
    def place(self):
        d: dict = {}
        for loc in self.STRUCTURE:
            d |= {loc: self.material}
        return d
    def register(self, loc: list[tuple[int, ...]]):
        self.loc = loc
        self.live_locations = list(loc)
        self.placed = True
    def check_destruction(self, game, *loc):
        from ..destruction import Destruction
        if self.destruction == Destruction.SOLID:
            return loc not in self.live_locations
        elif self.destruction == Destruction.DESTRUCTIBLE_SOFT:
            if loc in self.live_locations:
                self.live_locations.remove(loc)
            return True
        elif self.destruction == Destruction.DESTRUCTIBLE_HARD:
            if loc in self.live_locations:
                for key in self.live_locations:
                    game.board.mesh.states.set(game.board.mesh.states.bg, *key)
                self.live_locations = []
            return True
        elif self.destruction == Destruction.TOP_LAYER:
            def validate_wrapper():
                if game.player.location not in self.live_locations:
                    game.board.mesh.states.set(self.material, *loc)
            return validate_wrapper if loc in self.live_locations else True
        elif self.destruction == Destruction.PASSTHROUGH:
            def validate_wrapper():
                if tuple(game.player.location) not in self.live_locations:
                    game.board.mesh.states.set(self.material, *loc)
                    return False
            return validate_wrapper if loc in self.live_locations else True
    def tick(self, game, *loc):
        if loc in self.live_locations:
            self.on_touched()
        result = self.check_destruction(game, *loc)
        if not self.live_locations and not self.destroyed:
            self.on_destroyed()
            self.remove_tags(game)
            self.destroyed = True
        return result
    def remove_tags(self, game):
        for (x, y) in self.STRUCTURE:
            try:
                game.board.mesh.states_tm.remove_tag(f"{self.name}[x{x}y{y}]")
            except KeyError:
                ...

    # CALLBACKS:

    def on_touched(self):
        ...
    def on_destroyed(self):
        ...


class ShapeGenerator:
    STRUCTURE: list[tuple[int, ...]] = []
    EXTEND: list[tuple[int | float, ...]] = []
    PER_SIZE: list[tuple[int | float | None, ...]] = []
    @classmethod
    def generate_shape(cls, size: int, material, name: str | None = None, destruction = None):
        return cls.generate_template(size)(
            material=material,
            name=name,
            destruction=destruction,
        )
    @classmethod
    def generate_template(cls, size: int):
        new_structure = cls.STRUCTURE
        extend = cls.EXTEND
        per_size = []
        for s in range(1, size):
            for (x, y) in cls.PER_SIZE:
                if x is None:
                    x = s
                if y is None:
                    y = s
                per_size.append((x, y))
            extend += per_size
            for (x, y) in extend:
                if isinstance(x, float):
                    x = int(x) + s
                if isinstance(y, float):
                    y = int(y) + s
                new_structure.append((x, y))
        return type(
            f"{cls.__name__}X{size}",
            (BaseShape,),
            {
                "STRUCTURE": new_structure
            }
        )