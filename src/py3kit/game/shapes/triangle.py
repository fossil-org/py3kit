from . import ShapeGenerator

class Triangle(ShapeGenerator):
    STRUCTURE = [
        (0, 0)
    ]
    EXTEND = [
        (0.0, 0.0),
        (0.0, 0)
    ]
    PER_SIZE = [
        (0.0, None),
    ]