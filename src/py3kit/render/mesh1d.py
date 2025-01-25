from .mesh import MeshWithDimensions

class Mesh1D(MeshWithDimensions):
    DIMENSIONS = 1
    def __render__(self):
        if self.dimensions.get_type() != 2:
            from ..errors import RenderingError
            raise RenderingError(f"<Mesh1D> expected 1 dimension (x), got {self.dimensions.as_str_letters()}")
        line: str = ""
        for x in range(self.dimensions.get(1)):
            symbol = self.states.get(x, y)
            from .icon import Icon
            if not isinstance(symbol, Icon):
                raise TypeError(f"expected Icon, got {type(symbol)}")
            line += str(symbol)
        return line