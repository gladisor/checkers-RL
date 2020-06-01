import torch
import torch.nn as nn
import torch.nn.functional as F
from checkers import Checkers

class DQN(nn.Module):
	def __init__(self, d_in, d_hidden, num_hidden):
		super(DQN, self).__init__()
		self.in_layer = nn.Linear(d_in, d_hidden)

		self.hidden = nn.ModuleList()
		for _ in range(num_hidden):
			self.hidden.append(nn.Linear(d_hidden, d_hidden))
		self.out_layer = nn.Linear(d_hidden, 1)

	def forward(self, x):
		x = F.relu(self.in_layer(x))
		for layer in self.hidden:
			x = F.relu(layer(x))
		x = self.out_layer(x)
		return x

if __name__ == "__main__":
	q = DQN(d_in=96, d_hidden=64, num_hidden=5).float()

	env = Checkers()
	state = env.reset()
	state = torch.tensor(state).float()

	possible_actions = env.get_possible_actions('black')

	X = []
	for action in possible_actions:
		action = env.action_to_vect(action)
		action = torch.tensor(action).float()
		X.append(torch.cat((state, action)).float())

	X = torch.stack(X)
	q_vals = q(X)

	print(torch.argmax(q_vals))