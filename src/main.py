from py3kit import include

include.auto_globalize(globals())
include.fetch()

game = Game(Player(Piston(), 1, Icon("O"), (1, 8)), Board(Mesh2D(Dimensions(100, 30), StatesTagManager({"player": (1, 8)}, States({}, bg=".")))))
game.player.speed = 2
game.clear = False

lsh = ScriptHandler(LocalScript)
piston = Piston(game)

block = lsh.new("Block", Tile.generate_template(1))(Icon("X"), "BlockShape")

game.board.place(block, 8, 8)

while game.loop(output=lambda: (
    game.display_location(),
    game.display_out_of_bounds(else_call=lambda: (
        game.new_line()
    ))
)):
    piston.push("BlockShape[*]", "a")