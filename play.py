import tkinter as tk
from tkinter import messagebox
from train import TicTacToeEnv, QLearningAgent
import pickle

class TicTacToeGUI:
    def __init__(self, agent):
        self.agent = agent
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.env = TicTacToeEnv()  # Create the environment within the GUI
        self.initialize_board()

    def initialize_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, height=3, width=6,
                                               font=('Arial', 20), command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_click(self, row, col):
        if self.env.current_player == 1 and self.buttons[row][col]['text'] == "":
            self.make_move(row, col, "X")
            if not self.check_winner("X") and not self.is_board_full():
                self.env.current_player = -1
                self.agent_move()

    def agent_move(self):
        state = self.get_state()
        action = self.agent.choose_action(state, self.env.available_actions())
        if action and self.buttons[action[0]][action[1]]['text'] == "":
            self.make_move(action[0], action[1], "O")
            if not self.check_winner("O") and not self.is_board_full():
                self.env.current_player = 1

    def make_move(self, row, col, player_symbol):
        self.buttons[row][col]['text'] = player_symbol
        if self.check_winner(player_symbol) or self.is_board_full():
            messagebox.showinfo("Game Over", f"'{player_symbol}' wins!" if self.check_winner(player_symbol) else "It's a draw!")
            self.reset_board()

    def get_state(self):
        state = []
        for i in range(3):
            row = []
            for j in range(3):
                if self.buttons[i][j]['text'] == "X":
                    row.append(1)
                elif self.buttons[i][j]['text'] == "O":
                    row.append(-1)
                else:
                    row.append(0)
            state.append(row)
        return state

    def check_winner(self, player_symbol):
        for i in range(3):
            if all(self.buttons[i][j]['text'] == player_symbol for j in range(3)) or \
               all(self.buttons[j][i]['text'] == player_symbol for j in range(3)):
                return True
        if self.buttons[0][0]['text'] == player_symbol and self.buttons[1][1]['text'] == player_symbol and self.buttons[2][2]['text'] == player_symbol or \
           self.buttons[0][2]['text'] == player_symbol and self.buttons[1][1]['text'] == player_symbol and self.buttons[2][0]['text'] == player_symbol:
            return True
        return False

    def is_board_full(self):
        return all(self.buttons[i][j]['text'] != "" for i in range(3) for j in range(3))

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ""
        self.env.reset()

    def run(self):
        self.window.mainloop()

# Load the Q-table
def load_agent(filename='trained_agent.pkl'):
    with open(filename, 'rb') as file:
        Q_table = pickle.load(file)
    agent = QLearningAgent()
    agent.Q = Q_table
    return agent

# Load the trained agent
trained_agent = load_agent()

# Create and run the GUI
env = TicTacToeEnv()  # Create the environment for the agent to understand the game state
gui = TicTacToeGUI(trained_agent)
gui.run()
