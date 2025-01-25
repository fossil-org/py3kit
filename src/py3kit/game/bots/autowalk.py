class AutoWalk:
    def __init__(self, bot):
        self.bot = bot
    def enable(self):
        fn = self.bot.game.loop
        fn2 = lambda *args, **kwargs: (
            self.bot.walk(),
            fn(*args, **kwargs)
        )
        self.bot.game.loop = fn2