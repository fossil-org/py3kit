from .simple import SimpleBot

class ReverseBot(SimpleBot):
    def decide_action(self, do_action, do_opposite):
        do_opposite()