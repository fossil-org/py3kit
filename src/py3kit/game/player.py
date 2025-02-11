class Player:
    def __init__(
            self,
            piston,
            speed: int = 1,
            icon = None,
            location: tuple[int, ...] | None = None,
            states_tm = None
    ):
        self.piston = piston
        self.speed = speed
        self.oob = False
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
    def add_local_service(self, name: str, value=None):
        if callable(name) and value is None:
            self.set_local_service(name.__name__, name)
            return name
        self.set_local_service(name, value)
    def get_local_service(self, service: str):
        try:
            return self.services[service]
        except KeyError:
            raise NameError(f"Local player service '{service}' not found.")
    def set_local_service(self, service: str, value):
        self.services[service] = value
    def run_local_service(self, service: str, *args, **kwargs):
        return self.get_local_service(service)(*args, **kwargs)
    def move(self, action: str):
        result = self.piston.push(
            tag="player",
            action=action,
            distance=self.speed,
            shape=False,
            verbose_returns=True
        )
        self.location = result["location"]
        self.oob = result["oob"]

    # CALLBACKS:

    def on_death(self):
        from ..errors import PlayerNotFoundError
        raise PlayerNotFoundError(f"The player was not found on the board. This could be because the player tile was forcibly overwritten by another tile/shape.\nTIP FOR DEVELOPERS: this was triggered by game.player.on_death, you can create a script that changes what this callback does.")