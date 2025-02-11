from py3kit import include

include.auto_globalize(globals())
include.fetch()

lsh = ScriptHandler(LocalScript)
states = States.auto_convert_to_icon({(5, 5): "O"}, bg=Icon("."))
tm = StatesTagManager({"player": (5, 5)}, states=states)
mesh = Mesh2D(Dimensions(100, 30), tm)
board = Board(mesh)
piston = Piston()
player = Player(
    piston=piston,
    speed=2,
    icon=None,
    location=None,
    states_tm=tm
)
game = Game(player, board)

while game.loop(
    game.display_location,
    lambda: game.display_out_of_bounds(
        else_call=(
            game.display_last_move
        )
    )
):
    ...