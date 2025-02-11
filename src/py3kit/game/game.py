import os, readline

class Game:
    def __init__(
        self,
        player,
        *boards,
        **player_services
    ):
        self.boards = boards
        self.board = boards[0]
        self.session = {}
        from ..render.states_tm import StatesTagManager
        self.tm: StatesTagManager = self.board.mesh.states_tm
        from ..render.icon import Icon
        from .player import Player
        self.player: Player = player
        self.player.piston.game = self
        self.tm.states.set(Icon(self.player.icon), *self.player.location)
        self.last_action: str = ""
        self.after: list = []
        self.clear: bool = True
        self.output = ()
        player_services |= dict(
            game = self
        )
        self._add_player_services(**player_services)
    def _add_player_services(self, **services):
        for k, v in list(services.items()):
            self.player.add_local_service(k, v)
    def loop(self, *output):
        if self.clear: os.system("cls" if os.name == "nt" else "clear")
        if not self.output:
            self.output = output or (lambda: None,)
        for o in self.output:
            o()
        validate_wrapper_count: int = 0
        for i, (a, status) in enumerate(self.after):
            if status:
                result = a()
                if result is False:
                    self.after[i][1] = False
        for bot in self.board.bots:
            bot.ping()
        self.board.show()
        self.board.render()
        if str(self.tm.states.get(*self.player.location)) != str(self.player.icon):
            self.player.on_death()
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
            self.player.move(query)
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
            self.player.oob = set_oob
        else:
            self.tm.states.set(self.tm.states.bg, *self.player.location)
            self.player.location = original_location
            self.tm.states.set(self.player.icon, *self.player.location)
            self.player.oob = True

        self.tm.add_tag("player", *self.player.location)

        return True
    def add_output(self, *addition):
        output = self.output
        self.output = lambda: (
            *[o() for o in output],
            *[a() for a in addition]
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
        if self.player.oob:
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