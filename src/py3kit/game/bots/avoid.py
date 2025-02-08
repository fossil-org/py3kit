from .follower import FollowerBot

class AvoidBot(FollowerBot):
    def decide_action(self, do_action, do_opposite):
        do_opposite()