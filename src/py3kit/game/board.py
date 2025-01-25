class Board:
    def __init__(self, mesh):
        self.mesh = mesh
        self.shapes: list = []
        from ..render.checks import is_2d
        from ..errors import UnsupportedDimensionsError
        if not is_2d(self.mesh.dimensions):
            raise UnsupportedDimensionsError(f"Board can only be 2D, not {self.mesh.dimensions.get_type()}D")
    def show(self):
        from ..render.render import render
        print(render(self.mesh))
    def place(self, shape, *at):
        abs_loc_list: list = []
        for loc, icon in tuple(shape.place().items()):
            abs_loc = tuple(map(sum, zip(at, loc)))
            self.mesh.states.set(icon, *abs_loc)
            abs_loc_list.append(abs_loc)
            self.mesh.states_tm.add_tag(f"{shape.name}[x{loc[0]}y{loc[1]}]", *abs_loc)
        self.shapes.append((abs_loc_list, shape))
        shape.register(abs_loc_list)
        return shape.name
    def render(self):
        for loc, shape in self.shapes:
            for loc2, icon in tuple(shape.place().items()):
                abs_loc = tuple(map(sum, loc))
                self.mesh.states.set(icon, *abs_loc)