from initialize import *
import random

class QLearningAgent:
    def __init__(self, alpha, epsilon, discount_factor,symbol):
        self.Q = {}
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.symbol = symbol

    def get_Q_value(self, state, action):
        # Convert state to a tuple
        if isinstance(state, np.ndarray):
            state = tuple(state.flatten())
        # If (state, action) is not in Q, return 0.0
        if (state, action) not in self.Q:
            self.Q[(state, action)] = 0.0
        return self.Q[(state, action)]

    def choose_action(self, state, available_moves):
        """Choose an action among the available moves for the given state.
            use epsilon-greedy algorithm to choose the action."""
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(available_moves)
        else:
            # Choose the action with the highest Q value
            Q_values = [self.get_Q_value(state, action) for action in available_moves]
            max_Q = max(Q_values)
            if Q_values.count(max_Q) > 1: # if there are multiple actions with the same max Q value
                best_moves = [i for i in range(len(available_moves)) if Q_values[i] == max_Q]
                i = random.choice(best_moves)
            else:
                i = Q_values.index(max_Q)
            return available_moves[i]


    def update_Q_value(self, state, action, reward, next_state):
        game = TicTacToe()
        game.set_state(state.copy()) # set the state of the game to the current state
        # convert the state to a tuple
        state = tuple(state.flatten())
        next_state = tuple(next_state.flatten())
        # get the Q values for the next state
        next_Q_values = [self.get_Q_value(next_state, next_action) for next_action in game.available_moves()]
        max_next_Q = max(next_Q_values) if next_Q_values else 0.0 # if there are no available moves, set max_next_Q to 0.0
        self.Q[(state, action)] = self.Q.get((state, action), 0.0) + self.alpha * (reward + self.discount_factor * max_next_Q - self.Q.get((state, action), 0.0)) # update Q value

class RandomPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def choose_action(self, available_moves):
        return random.choice(available_moves)

def train(num_episodes, alpha, epsilon, discount_factor, opponent):
    """Train the agent for num_episodes episodes. Return the trained agent."""
    agent = QLearningAgent(alpha, epsilon, discount_factor, 'X')
    for i in range(num_episodes):
        game = TicTacToe()
        game.current_player = random.choice(game.players) # Randomly choose the first player
        while not game.game_over:
            state = game.board.copy()
            if game.current_player == agent.symbol: # agent's turn
                action = agent.choose_action(state, game.available_moves())
            else: # opponent's turn
                action = opponent.choose_action(game.available_moves())
            game.make_move(action) 
            next_state = game.board.copy() # get the next state
            game.switch_player()
            
            if game.game_over:
                if game.winner == agent.symbol:
                    reward = 1
                elif game.winner is None:
                    reward = 0.5
                else:
                    reward = 0
                # update Q value when game is over
                agent.update_Q_value(state, action, reward, next_state)
        game.reset()
    return agent

def test(agent,num_games, opponent):
    num_wins = 0
    for i in range(num_games):
        game = TicTacToe()
        game.current_player = random.choice(game.players)
        while not game.game_over:
            state = game.board.copy()
            if game.current_player == agent.symbol:
                action = agent.choose_action(state, game.available_moves())
            else:
                action = opponent.choose_action(game.available_moves())
            game.make_move(action)
            game.switch_player()
        if game.winner == agent.symbol:
            num_wins += 1
        game.reset()

    return num_wins / num_games

if __name__ == "__main__":
    num_episodes = 10000 # number of episodes to train the agent
    alpha = 0.1
    epsilon = 0.1 # exploration rate
    discount_factor = 0.9 # discount factor
    opponent = RandomPlayer('O')
    agent = train(num_episodes, alpha, epsilon, discount_factor, opponent)
    num_games = 1000
    win_rate = test(agent, num_games, opponent)
    print(f"Win rate: {win_rate}")
    # print(agent.Q)