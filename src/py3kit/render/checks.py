def is_1d(dimensions):
    return dimensions.get_type() == 1
def is_2d(dimensions):
    return dimensions.get_type() == 2
def is_3d(dimensions):
    return dimensions.get_type() == 3
def is_renderable(obj):
    return hasattr(obj, "__render__")