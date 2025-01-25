class MeshWithDimensions:
    DIMENSIONS = 0
    def __init__(self, dimensions, states_tm):
        self.dimensions = dimensions
        self.states_tm = states_tm
        self.states = states_tm.states