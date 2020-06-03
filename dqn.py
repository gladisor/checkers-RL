import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
	def __init__(self, d_in=96, d_hidden=64, num_hidden=5):
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