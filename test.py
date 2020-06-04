from arena import Arena
from dqn import DQN
from game import Checkers
import torch
import torch.nn as nn

env = Checkers()
env.reset()
env.render()
# agent = DQN()
# opponent = DQN()

# player1 = lambda x: torch.argmax(agent(x))
# player2 = lambda x: torch.argmax(opponent(x))

# arena = Arena(DQN, env)
# looser, data = arena.play_game(player1, player2, display=True)