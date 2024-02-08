import numpy as np
import random

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.players = ["X", "O"]
        self.current_player = "X"
        self.winner = None
        self.game_over = False

    def reset(self):
        self.board = np.zeros((3, 3))
        self.current_player = None
        self.winner = None
        self.game_over = False

    def available_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0: # move is available
                    moves.append((i, j))
        return moves

    def make_move(self, move):
        # move is a tuple (i, j)
        if self.board[move[0]][move[1]] != 0:
            return False
        self.board[move[0]][move[1]] = self.players.index(self.current_player) + 1
        self.check_winner() # check if the move is a winning move
        self.check_tie() # check if the game is a tie
        self.switch_player()
        return True

    def set_state(self, state):
        self.board = np.array(state).reshape(3, 3)

    def switch_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def check_winner(self):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                self.winner = self.players[int(self.board[i][0] - 1)]
                self.game_over = True
        # Check columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != 0:
                self.winner = self.players[int(self.board[0][j] - 1)]
                self.game_over = True
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            self.winner = self.players[int(self.board[0][0] - 1)]
            self.game_over = True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            self.winner = self.players[int(self.board[0][2] - 1)]
            self.game_over = True

    def check_tie(self):
        ## check if all positions are filled if so then self.game_over = True
        if all([self.board[i][j] != 0 for i in range(3) for j in range(3)]):
            self.game_over = True

    def print_board(self):
        for i in range(3):
            for j in range(3):
                print("|", end=" ")
                print(self.players[int(self.board[i][j] - 1)] if self.board[i][j] != 0 else " ", end=" ")
            print("|\n")
