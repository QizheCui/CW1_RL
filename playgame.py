from initialize import *

game = TicTacToe()
game.current_player = game.players[0]
game.print_board()

# Play the game
while not game.game_over:
    move = input(f"'{game.current_player}'s turn. Enter row and column (e.g. 0 0): ")
    move = tuple(map(int, move.split())) # e.g. "0 0" -> (0, 0)
    while move not in game.available_moves(): # move is invalid
        move = input("Invalid move. Try again: ") # ask for another move
        move = tuple(map(int, move.split())) # e.g. "0 0" -> (0, 0)
    game.make_move(move)
    game.print_board()

if game.winner:
    print(f"{game.winner} wins!")
else:
    print("It''s a tie!")