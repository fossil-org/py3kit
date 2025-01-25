class States:
    def __init__(
        self,
        states: dict[tuple[int, ...], str],
        *,
        bg: str | None = None
    ):
        self.states: dict[tuple[int, ...], str] = states
        from ..render.icon import Icon
        self.bg: Icon = Icon(bg or " ")
    def set(self, icon, *dimensions):
        self.states[dimensions] = icon
    def get(self, *dimensions, use_bg: bool = True):
        return self.states.get(dimensions, self.bg if use_bg else None)
    @classmethod
    def auto_convert_to_icon(
        cls,
        states: dict[tuple[int, ...], str],
        *,
        bg: str | None = None,
    ):
        from .icon import Icon

        return cls(
            dict((k, Icon(v)) for k, v in list(states.items())),
            bg=Icon(bg)
        )