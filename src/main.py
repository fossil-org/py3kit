from py3kit import include

include.auto_globalize(globals())
include.fetch()

game = Game(Player(Icon("O"), (9, 10), 1), Board(Mesh2D(Dimensions(100, 30), StatesTagManager({"player": (5, 5)}, States({}, bg=".")))))
game.player.speed = 2

lsh = ScriptHandler(LocalScript)
piston = Piston(game)

def main():
    bot = lsh.new("Bot1", FollowerBot)(Icon("#"), game, piston, (20, 20), "player")
    auto_walk = AutoWalk(bot)
    auto_walk.enable()

button = lsh.new("Button1", Tile.generate_template(1), main=main)(Icon("@"), destruction=Destruction.DESTRUCTIBLE_HARD)

game.board.place(button, 8, 8)

while game.loop(output=lambda: (
    game.display_location(),
    game.display_out_of_bounds(else_call=lambda: (
        game.new_line()
    ))
)):
    ...