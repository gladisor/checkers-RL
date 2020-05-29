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
	q = DQN(d_in=96, d_hidden=10, num_hidden=5).float()

	env = Checkers()
	state = env.reset()
	action = ((2, 0), (3, 1))
	action_vect = env.action_to_vect(action)

	state = torch.tensor(state)
	action_vect = torch.tensor(action_vect)
	x = torch.cat((state, action_vect)).float()

	print(q)
	print(q(x))