class RandomChoice:
    def __init__(self, choices):
        self.choices = choices
    def __call__(self):
        import random
        return random.choice(self.choices)

def get_random_choice(choices):
    return RandomChoice(choices)()