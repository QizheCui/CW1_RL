import numpy as np
import random
from itertools import product
import pickle

# Tic-Tac-Toe environment
class TicTacToeEnv:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.current_player = 1  # Player 1 starts
        self.done = False
        self.winner = None

    def reset(self):
        self.board = np.zeros((3, 3))
        self.current_player = 1
        self.done = False
        self.winner = None
        return self.board

    def step(self, action):
        if self.done or self.board[action] != 0:
            return self.board, 0, self.done

        # Perform action
        self.board[action] = self.current_player

        # Check for win or draw
        if self.check_winner():
            self.done = True
            reward = 1
        elif np.all(self.board != 0):
            self.done = True
            reward = 0.5  # Draw
        else:
            reward = 0
            self.current_player = -self.current_player  # Change turn

        return self.board, reward, self.done

    def check_winner(self):
        # Check rows, columns and diagonals
        for i in range(3):
            if np.all(self.board[i, :] == self.current_player) or \
               np.all(self.board[:, i] == self.current_player):
                self.winner = self.current_player
                return True

        if self.board[0, 0] == self.current_player and self.board[1, 1] == self.current_player and self.board[2, 2] == self.current_player or \
           self.board[0, 2] == self.current_player and self.board[1, 1] == self.current_player and self.board[2, 0] == self.current_player:
            self.winner = self.current_player
            return True

        return False

    def available_actions(self):
        return [tuple(action) for action in np.argwhere(self.board == 0)]

    def render(self):
        symbols = {0: '.', 1: 'X', -1: 'O'}
        for row in self.board:
            print(' '.join([symbols[cell] for cell in row]))

# Simple Q-Learning Agent
class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=1, epsilon=0.2):
        self.Q = {}  # State-action pairs
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def get_Q(self, state, action):
        return self.Q.get((tuple(map(tuple, state)), action), 0)

    def choose_action(self, state, available_actions):
        if random.uniform(0, 1) < self.epsilon:
            # Explore
            return random.choice(available_actions)
        else:
            # Exploit
            Q_values = [self.get_Q(state, action) for action in available_actions]
            max_Q = max(Q_values)
            # In case multiple actions have the same value, randomly choose one of them
            return random.choice([action for action, Q in zip(available_actions, Q_values) if Q == max_Q])

    def update_Q(self, state, action, reward, next_state, next_available_actions):
        max_future_Q = max([self.get_Q(next_state, next_action) for next_action in next_available_actions], default=0)
        current_Q = self.get_Q(state, action)
        new_Q = current_Q + self.alpha * (reward + self.gamma * max_future_Q - current_Q)
        self.Q[(tuple(map(tuple, state)), action)] = new_Q

# Training the Agent
def train_agent(episodes=10000):
    env = TicTacToeEnv()
    agent = QLearningAgent()
    random_player = -1  # Assuming agent is 1, random player is -1

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            # Agent's turn
            if env.current_player == 1:
                action = agent.choose_action(state, env.available_actions())
                next_state, reward, done = env.step(action)
                agent.update_Q(state, action, reward, next_state, env.available_actions())

            # Random player's turn
            else:
                available_actions = env.available_actions()
                if available_actions:
                    action = random.choice(available_actions) # random action
                    next_state, _, done = env.step(action)

            state = next_state

    return agent

def evaluate_agent(agent, num_games=1000):
    env = TicTacToeEnv()
    random_player = -1  # Assuming agent is 1, random player is -1
    results = {"Agent Wins": 0, "Random Wins": 0, "Draws": 0}

    for _ in range(num_games):
        state = env.reset()
        done = False

        while not done:
            # Agent's turn
            if env.current_player == 1:
                action = agent.choose_action(state, env.available_actions())
                state, _, done = env.step(action)
                if done:
                    if env.winner == 1:
                        results["Agent Wins"] += 1
                    elif env.winner is None:
                        results["Draws"] += 1

            # Random player's turn
            else:
                available_actions = env.available_actions()
                if available_actions:
                    action = random.choice(available_actions)
                    state, _, done = env.step(action)
                    if done and env.winner == -1:
                        results["Random Wins"] += 1

    return results




# Save the Q-table
def save_agent(agent, filename='trained_agent.pkl'):
    with open(filename, 'wb') as file:
        pickle.dump(agent.Q, file)

# Save the trained agent's Q-table
# save_agent(trained_agent)


# Train the agent
trained_agent = train_agent(episodes=50000)


# Evaluate the trained agent
evaluation_results = evaluate_agent(trained_agent, num_games=1000)

# Print the results
print("Evaluation Results:")
for result, count in evaluation_results.items():
    print(f"{result}: {count}")

