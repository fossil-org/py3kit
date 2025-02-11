class StatesTagManager:
    def __init__(self, tags: dict[str, tuple[int,...]], *, states):
        self.tags: dict[str, tuple[int, ...]] = tags
        self.protected: list[tuple[int, ...]] = []
        self.states = states
    def get_location_by_tag(self, tag: str):
        try:
            return self.tags[tag]
        except KeyError:
            from ..errors import TagNotFoundError
            raise TagNotFoundError(f"Tag '{tag}' does not exist.") from None
    def get_icon_by_tag(self, tag: str):
        return self.states.get(*self.get_location_by_tag(tag))
    def add_tag(self, tag: str, *dimensions):
        self.set_tag(tag, *dimensions)
    def set_tag(self, tag: str, *dimensions):
        self.tags[tag] = dimensions
    def remove_tag(self, tag: str):
        self.tags.pop(tag)
    def tag_exists(self, tag: str):
        return tag in list(self.tags.keys())
    def move_tag(self, tag: str, *new, icon = None):
        location = self.tags[tag]
        icon = icon or self.states.get(*location)

        self.tags[tag] = new
        self.states.set(icon, *self.tags[tag])
        if list(location) not in self.protected:
            self.states.set(self.states.bg, *location)