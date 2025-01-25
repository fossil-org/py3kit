class Player:
    def __init__(
            self,
            icon,
            location: tuple[int, ...],
            speed: int,
            states_tm = None
    ):
        self.icon = icon
        if icon is None:
            from ..errors import AutoFindError
            if not states_tm:
                raise AutoFindError("Icon cannot be None (auto-find) if the states_tm parameter is not fulfilled.")
            if not states_tm.tag_exists("player"):
                raise AutoFindError("Icon cannot be None (auto-find) if the states_tm object provided does not have a tag called 'player'")
            self.icon = states_tm.get_icon_by_tag("player")
        self.location: list[int] = list(location)
        self.speed: int = speed