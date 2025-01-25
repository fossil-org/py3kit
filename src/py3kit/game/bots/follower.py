from .simple import SimpleBot

class FollowerBot(SimpleBot):
    def __init__(self, icon, game, piston, location, target_tag, name = None, speed = 1):
        self.target_tag = target_tag
        super().__init__(icon, game, piston, location, game.tm.get_location_by_tag(target_tag), name, speed)
    def walk(self):
        self.target = self.game.tm.get_location_by_tag(self.target_tag)
        super().walk()