import os, readline

class Game:
    def __init__(
        self,
        player,
        *boards
    ):
        self.boards = boards
        self.board = boards[0]
        self.session = {}
        from ..render.states_tm import StatesTagManager
        self.tm: StatesTagManager = self.board.mesh.states_tm
        from ..render.icon import Icon
        from .player import Player
        self.player: Player = player
        self.tm.states.set(Icon(self.player.icon), *self.player.location)
        self.out_of_bounds: bool = False
        self.last_action: str = ""
        self.after: list = []
        self.clear: bool = True
        self.output = None
    def loop(self, *, output=None):
        if self.clear: os.system("cls" if os.name == "nt" else "clear")
        if not self.output:
            self.output = output or (lambda: ...)
        self.output()
        validate_wrapper_count: int = 0
        for i, (a, status) in enumerate(self.after):
            if status:
                result = a()
                if result is False:
                    self.after[i][1] = False
        self.board.show()
        self.board.render()
        if str(self.tm.states.get(*self.player.location)) != str(self.player.icon):
            from ..errors import PlayerNotFoundError
            raise PlayerNotFoundError(f"The player was not found on the board. This could be because of the player tile being forcibly overwritten by another tile/shape.")
        try:
            query: str = input("* ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            exit()
        self.last_action = query
        if not query:
            return True
        from ..render.icon import Icon
        set_oob: bool = False
        original_location: list = list(self.player.location)
        if query in tuple("qweasdzxc"):
            for _ in range(self.player.speed):
                if self.validate_location():
                    original_location = list(self.player.location)
                    updated_x = self.player.location[0] + {
                        "q": -1, "w": 0, "e": 1,
                        "a": -1, "s": 0, "d": 1,
                        "z": -1, "x": 0, "c": 1
                    }[query]
                    updated_y = self.player.location[1] + {
                        "q": 1,  "w": 1,  "e": 1,
                        "a": 0,  "s": -1, "d": 0,
                        "z": -1, "x": -1, "c": -1
                    }[query]
                    passed: int = 0
                    total: int = len(self.board.shapes)
                    for _, shape in self.board.shapes:
                        result = shape.tick(self, updated_x, updated_y)
                        if result:
                            passed += 1
                            if callable(result):
                                self.after.append([result, True])
                    if passed >= total:
                        self.tm.states.set(self.tm.states.bg, *self.player.location)
                        self.player.location[0] = updated_x
                        self.player.location[1] = updated_y
                        self.tm.states.set(self.player.icon, *self.player.location)
                    else:
                        set_oob = True
                        break
        elif query.startswith("eval::"):
            try:
                game = self
                print(f"{query.removeprefix('eval::')} = {eval(query.removeprefix('eval::'))}")
            except Exception as err:
                print(f"Error: {err}")
        elif query.startswith("exec::"):
            try:
                game = self
                exec(f"{query.removeprefix('exec::')}")
            except Exception as err:
                print(f"Error: {err}")
        elif query == "clear":
            self.clear = not self.clear
            print(f"Clear screen set to {self.clear}")

        if self.validate_location():
            self.out_of_bounds = set_oob
        else:
            self.tm.states.set(self.tm.states.bg, *self.player.location)
            self.player.location = original_location
            self.tm.states.set(self.player.icon, *self.player.location)
            self.out_of_bounds = True

        self.tm.add_tag("player", *self.player.location)

        return True
    def add_output(self, addition):
        output = self.output
        self.output = lambda: (
            output(),
            addition()
        )
    def get_player_location(self):
        return tuple(self.player.location)
    def validate_location(self):
        return not any([
            self.player.location[0] < 0,
            self.player.location[0] >= self.board.mesh.dimensions.get(1),
            self.player.location[1] < 0,
            self.player.location[1] >= self.board.mesh.dimensions.get(2)
        ])

    def display_location(self, text: str | None = None):
        print((text or "x{x} y{y}").format(x=self.player.location[0], y=self.player.location[1]))
    def display_out_of_bounds(self, text: str | None = None, else_call = None):
        if self.out_of_bounds:
            print(text or "Cannot go there")
        elif else_call:
            else_call()
    def display_last_move(self, text: str | None = None, else_call = None):
        if self.last_action in tuple("qweasdzxc"):
            print((text or "{}".format({
                "q": "🢄", "w": "🢁", "e": "🢅",
                "a": "🢀", "s": "🢃", "d": "🢂",
                "z": "🢇", "x": "🢃", "c": "🢆"
            }[self.last_action])))
        else:
            (else_call or print)()
    def display_text(self, text: str | None = None, inline: bool = False):
        print(text, end="" if inline else "\n")
    def new_line(self):
        print()