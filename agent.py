from dqn import DQN
import numpy as np
import torch

class Agent():
	def __init__(self, dqn, epsilon):
		self.dqn = dqn
		self.epsilon = epsilon

	def choose_action_egreedy(self, state_actions):
		if torch.rand(1) > self.epsilon:
			action = torch.argmax(self.dqn(state_actions))
		else:
			action = np.random.randint(len(state_actions))
		return action