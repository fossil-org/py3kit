class Piston:
    def __init__(self, game):
        self.game = game
        self.icon = None
    def push(self, tag, action, length = 1, shape = True, icon = None, from_shape_push = False):
        if tag.endswith("[*]"):
            tag = tag.removesuffix("[*]")
            icon = self.game.tm.get_icon_by_tag(tag + "[x0y0]")
            for _, shape in self.game.board.shapes:
                if shape.name == tag:
                    for i, loc in enumerate(shape.live_locations):
                        for _ in range(length):
                            shape.live_locations[i] = [x+y for (x, y) in zip(shape.live_locations[i], self._create_offset(action))]
                    for i, loc in enumerate(shape.loc):
                        for _ in range(length):
                            shape.loc[i] = [x+y for (x, y) in zip(shape.loc[i], self._create_offset(action))]
                    break
            else:
                from ..errors import ShapeNotFoundError
                raise ShapeNotFoundError("Cannot move a shape that does not exist. Specifying shape=False could resolve the issue.")
            for sub_tag in [st for st in self.game.tm.tags if "[".join(st.split("[")[:-1]) == tag]:
                self.push(sub_tag, action, length, icon, from_shape_push=True)
            self.game.tm.protected = []
        elif self.game.tm.tag_exists(tag):
            location = self.game.tm.get_location_by_tag(tag)
            new_location = [x+y for x, y in zip(location, self._create_offset(action))]
            if not self.validate_location(*new_location):
                return location
            passed: int = 0
            total: int = len(self.game.board.shapes)
            for _, shape in self.game.board.shapes:
                result = shape.tick(self.game, updated_x, updated_y)
                if result:
                    passed += 1
                    if callable(result):
                        self.game.after.append([result, True])
            if passed >= total:
                if from_shape_push:
                    self.game.tm.protected.append(new_location)
                self.game.tm.apply_offset(tag, *self._create_offset(action), icon=icon)
                return new_location
            else:
                return location
        else:
            from ..errors import TagNotFoundError
            raise TagNotFoundError("Cannot push a non-existent tag.")
    def validate_location(self, *location):
        return not any([
            location[0] < 0,
            location[0] >= self.game.board.mesh.dimensions.get(1),
            location[1] < 0,
            location[1] >= self.game.board.mesh.dimensions.get(2)
        ])
    def _create_offset(self, action):
        return ({
            "q": -1, "w": 0, "e": 1,
            "a": -1, "s": 0, "d": 1,
            "z": -1, "x": 0, "c": 1
        }[action], {
            "q": 1, "w": 1, "e": 1,
            "a": 0, "s": -1, "d": 0,
            "z": -1, "x": -1, "c": -1
        }[action])