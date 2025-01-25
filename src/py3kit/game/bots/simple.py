class SimpleBot:
    def __init__(self, icon, game, piston, location, target, name = None, speed = 1):
        self.game = game
        from random import randint
        self.name = name or f"{self.__class__.__name__}N{str(randint(1, 999))}"
        self.piston = piston
        self.icon = icon
        self.location = location
        self.target = target
        self.speed = speed
        self.enabled = True

        self.game.tm.states.set(self.icon, *self.location)
        self.game.tm.add_tag(self.name, *self.location)

    def walk(self):
        if not self.enabled or self.location == self.target:
            return
        right = self.target[0] > self.location[0]
        left = self.target[0] < self.location[0]
        up = self.target[1] > self.location[1]
        down = self.target[1] < self.location[1]
        action = None

        if left and up:
            action = "q"
        elif right and up:
            action = "e"
        elif left and down:
            action = "z"
        elif right and down:
            action = "c"
        elif up:
            action = "w"
        elif down:
            action = "x"
        elif left:
            action = "a"
        elif right:
            action = "d"

        opposite = {
            "q": "c",
            "w": "x",
            "e": "z",
            "a": "d",
            "s": "w",
            "d": "a",
            "z": "e",
            "x": "w",
            "c": "q"
        }[action]


        self.location = self.piston.push(self.name, action, self.speed, False)

        if tuple(self.location) == self.target:
            loc = self.location
            self.game.tm.states.set(self.game.player.icon, *loc)
            self.enabled = False
            self.on_arrived()

    # CALLBACKS:

    def on_arrived(self):
        ...