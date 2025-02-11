class Piston:
    def __init__(self, game = None):
        self.game = game
        self.icon = None
    def push(self, tag, action, distance = 1, shape = True, icon = None, verbose_returns = False, from_shape_push = False):
        seen = []
        oob = False
        for i in range(distance):
            result = self._push_1(tag, action, shape, icon, from_shape_push)
            if result in seen:
                oob = True
            seen.append(result)
        return {
            "location": result, # NOQA
            "path": seen,
            "oob": oob
        } if verbose_returns else result # NOQA
    def _push_1(self, tag, action, shape = True, icon = None, from_shape_push = False):
        if self.game is None:
            raise ValueError("piston.game must be specified to use this piston.")
        if tag.endswith("[*]"):
            tag = tag.removesuffix("[*]")
            icon = self.game.tm.get_icon_by_tag(tag + "[x0y0]")
            for _, shape in self.game.board.shapes:
                if shape.name == tag:
                    for i, loc in enumerate(shape.live_locations):
                        for _ in range(distance):
                            shape.live_locations[i] = [x+y for (x, y) in zip(shape.live_locations[i], self.create_offset(action))]
                    for i, loc in enumerate(shape.loc):
                        for _ in range(distance):
                            shape.loc[i] = [x+y for (x, y) in zip(shape.loc[i], self.create_offset(action))]
                    break
            else:
                from ..errors import ShapeNotFoundError
                raise ShapeNotFoundError("Cannot move a shape that does not exist. Specify shape=False if you want to push a tag.")
            for sub_tag in [st for st in self.game.tm.tags if "[".join(st.split("[")[:-1]) == tag]:
                self.push(sub_tag, action, distance, icon, from_shape_push=True)
            self.game.tm.protected = []
        elif self.game.tm.tag_exists(tag):
            location = list(self.game.tm.get_location_by_tag(tag))
            new_location = self.apply_offset(location, self.create_offset(action))
            passed: int = 0
            total: int = len(self.game.board.shapes)
            for _, shape in self.game.board.shapes:
                result = shape.tick(self.game, *new_location)
                if result:
                    passed += 1
                    if callable(result):
                        self.game.after.append([result, True])
            if passed >= total and self.validate_location(*new_location):
                if from_shape_push:
                    self.game.tm.protected.append(new_location)
                self.game.tm.move_tag(tag, *new_location, icon=icon)
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
    @staticmethod
    def create_offset(action, amount = 1):
        return ({
            "q": -amount, "w": 0, "e": amount,
            "a": -amount, "s": 0, "d": amount,
            "z": -amount, "x": 0, "c": amount
        }[action], {
            "q": amount, "w": amount, "e": amount,
            "a": 0, "s": -amount, "d": 0,
            "z": -amount, "x": -amount, "c": -amount
        }[action])
    @staticmethod
    def apply_offset(location, offset):
        return [x+y for (x, y) in zip(location, offset)]