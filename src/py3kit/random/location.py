class RandomLocation:
    def __init__(self, dimensions: int, min_value: int, max_value: int):
        self.dimensions = dimensions
        self.min_value = min_value
        self.max_value = max_value
    def __call__(self):
        import random
        r = []
        for dimension in range(self.dimensions):
            r.append(random.randint(self.min_value, self.max_value))
        return r

def get_random_location(dimensions: int, min_value: int, max_value: int):
    return RandomLocation(dimensions, min_value, max_value)()