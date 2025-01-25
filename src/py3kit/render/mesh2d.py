from .mesh import MeshWithDimensions

class Mesh2D(MeshWithDimensions):
    DIMENSIONS = 2
    def __render__(self):
        if self.dimensions.get_type() != 2:
            from ..errors import RenderingError
            raise RenderingError(f"<Mesh2D> expected 2 dimensions (x, y), got {self.dimensions.as_str_letters()}")
        lines: list[str] = []
        for y in range(self.dimensions.get(2)):
            line = ""
            for x in range(self.dimensions.get(1)):
                symbol = self.states.get(x, y)
                from .icon import Icon
                if not isinstance(symbol, Icon):
                    raise TypeError(f"expected Icon, got {type(symbol)}")
                line += str(symbol)
            lines.append(line)
        return "\n".join(reversed(lines))