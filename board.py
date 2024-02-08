import numpy as np

# step1: set up the environment
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        # Print the board
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        # print out the index of the available moves
        return [i for i, x in enumerate(self.board) if x == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter # make the move
            if self.winner(square, letter): # check if the move is a winning move
                self.current_winner = letter # update the winner   
            return True # return True if the move is valid
        return False # return False if the move is invalid

    def winner(self, square, letter):
        # Check the row
        row_ind = square // 3 # first row is 0, second row is 1, third row is 2
        row = self.board[row_ind*3:(row_ind+1)*3] # get the row, e.g. [0, 1, 2], [3, 4, 5], [6, 7, 8]
        if all([s == letter for s in row]):
            return True

        # Check the column
        col_ind = square % 3 # first column is 0, second column is 1, third column is 2
        column = [self.board[col_ind+i*3] for i in range(3)] # get the column, e.g. [0, 3, 6], [1, 4, 7], [2, 5, 8]
        if all([s == letter for s in column]):
            return True

        # Check diagonals
        if square % 2 == 0: # check 0 4 8 or 2 4 6
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def gameover(self, letter):
        return self.winner(letter) or self.tie()

    def tie(self):
        # all the spaces are filled
        return all([s != ' ' for s in self.board])

    def reset(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

# step2: simple RL agent

class RLAgent:
    def __init__(self, alpha=0.1, gamma=0.9):
        self.alpha = alpha
        self.gamma = gamma
        self.Q = {}  # state-action pair to value
        self.epsilon = 0.2  # exploration rate/ epsilon

    def get_state(self, game):
        return str(game.board)

    def update_Q(self, state, next_state, action, reward):
        max_future_q = max(self.Q.get(next_state, {}).values(), default=0)
        current_q = self.Q.get(state, {}).get(action, 0)
        new_q = (1 - self.alpha) * current_q + self.alpha * (reward + self.gamma * max_future_q)
        self.Q.setdefault(state, {})[action] = new_q

    def choose_action(self, state, available_actions):
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(available_actions)
        else:
            q_values = self.Q.get(state, {})
            action = max(available_actions, key=lambda x: q_values.get(x, 0))
        return action

# step3: random opponent
class RandomPlayer:
    def choose_action(self, available_actions):
        return np.random.choice(available_actions)

# winningmoveplayer
class WinningMovePlayer:
    def __init__(self, letter):
        self.letter = letter

    def choose_action(self, game):
        # First, check if a winning move is available
        for move in game.available_moves():
            temp_board = game.board.copy()
            temp_board[move] = self.letter
            if game.winner(move, self.letter):
                return move

        # If no winning move, pick randomly
        return np.random.choice(game.available_moves())



# step4: training loop
def play_game(agent, game, player, reward=0):
    current_player = agent

    while True:
        state = agent.get_state(game)

        if current_player == agent:
            action = agent.choose_action(state, game.available_moves())
            game.make_move(action, 'X')
            next_state = agent.get_state(game)
            agent.update_Q(state, next_state, action, reward)
        else:
            # Make sure to pass the whole game object, not just the board
            action = player.choose_action(game)
            game.make_move(action, 'O')

        if game.current_winner or len(game.available_moves()) == 0:
            if game.current_winner == 'X':
                agent.update_Q(state, next_state, action, reward)
            return

        current_player = player if current_player == agent else agent

"""
# Initialize game, agent, and opponent
game = TicTacToe()
agent = RLAgent() 
random_player = RandomPlayer()

# Train the agent
for _ in range(10000):
    game.reset()
    play_game(agent, game, random_player) # train my agent
"""

# Initialize game, agent, and WinningMovePlayer
game = TicTacToe()
agent = RLAgent()
winning_move_player = WinningMovePlayer('O')

# Train the agent
for _ in range(10000):  # Increase the number of training games as needed
    game.reset()
    play_game(agent, game, winning_move_player)


# evaluation
def evaluate_agent(agent, opponent, num_games=100):
    agent_wins = 0
    opponent_wins = 0
    draws = 0

    for _ in range(num_games):
        game.reset()
        current_player = agent

        while True:
            state = agent.get_state(game)

            if current_player == agent:
                action = agent.choose_action(state, game.available_moves())
                game.make_move(action, 'X')
            else:
                action = opponent.choose_action(game.available_moves())
                game.make_move(action, 'O')

            if game.current_winner:
                if game.current_winner == 'X':
                    agent_wins += 1
                else:
                    opponent_wins += 1
                break

            if len(game.available_moves()) == 0:
                draws += 1
                break

            current_player = opponent if current_player == agent else agent

    print(f"Agent wins: {agent_wins} / {num_games}, Opponent wins: {opponent_wins} / {num_games}, Draws: {draws} / {num_games}")

evaluate_agent(agent, RandomPlayer(), num_games=1000)
# evaluate_agent(agent, WinningMovePlayer(), num_games=100)
# evaluate_agent(agent, DefensivePlayer(), num_games=100)
