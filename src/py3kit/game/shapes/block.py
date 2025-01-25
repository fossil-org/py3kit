from . import ShapeGenerator

class Block(ShapeGenerator):
    STRUCTURE = [
        (0, 0)
    ]
    EXTEND = [
        (0.0, 0),
        (0, 0.0),
        (0.0, 0.0),
    ]
    PER_SIZE = [
        (0.0, None),
        (None, 0.0)
    ]