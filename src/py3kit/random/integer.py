class RandomInteger:
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value
    def __call__(self):
        import random
        return random.randint(self.min_value, self.max_value)

def get_random_integer(min_value: int, max_value: int):
    return RandomInteger(min_value, max_value)()