class ShapeBuilder:
    def __init__(self):
        ...
    def build_shape(self, shape_name: str):
        from importlib import import_module

        module_name: str = ""
        upper: bool = False

        for char in shape_name:
            if char.isupper():
                if upper:
                    module_name += "_"
                module_name += char.lower()
                upper = True
            else:
                module_name += char
        try:
            return getattr(import_module(f"py3kit.game.shapes.{module_name}"), shape_name)
        except Exception:
            from ...render.errors import BuildError
            raise BuildError(f"Shape {shape_name} could not be found.")
    def __getattr__(self, shape_name: str):
        return self.build_shape(shape_name)