class Player:
    def __init__(
            self,
            piston,
            speed: int = 1,
            icon = None,
            location: tuple[int, ...] | None = None,
            opo = None,
            states_tm = None
    ):
        self.piston = piston
        self.speed = speed
        self.icon = icon
        if icon is None:
            from ..errors import AutoFindError
            if not states_tm:
                raise AutoFindError("Icon cannot be None (auto-find) if the states_tm parameter is not fulfilled.")
            if not states_tm.tag_exists("player"):
                raise AutoFindError("Icon cannot be None (auto-find) if the states_tm object provided does not have a tag called 'player'")
            self.icon = states_tm.get_icon_by_tag("player")
        self.location: list[int] = location
        if location is None:
            from ..errors import AutoFindError
            if not states_tm:
                raise AutoFindError("Location cannot be None (auto-find) if the states_tm parameter is not fulfilled.")
            if not states_tm.tag_exists("player"):
                raise AutoFindError("Location cannot be None (auto-find) if the states_tm object provided does not have a tag called 'player'")
            self.location = states_tm.get_location_by_tag("player")
        self.location = list(self.location)
        self.services: dict = {}
    def add_player_service(self, name: str, value):
        self.services |= {name: value}
    def get_player_service(self, service: str):
        return self.services.get(service)
    def run_player_service(self, service: str, *args, **kwargs):
        return self.get_player_service(service)(*args, **kwargs)
    def move(self, action: str):
        self.piston.push(
            tag="player",
            action=action,
            distance=self.speed,
            shape=False
        )

    # CALLBACKS:

    def on_death(self):
        from ..errors import PlayerNotFoundError
        raise PlayerNotFoundError(f"The player was not found on the board. This could be because the player tile was forcibly overwritten by another tile/shape.\nTIP FOR DEVELOPERS: this was triggered by game.player.on_death, you can create a script that changes what this callback does.")