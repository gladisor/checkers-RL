from game import Checkers
from dqn import DQN
from arena import Arena
from tqdm import tqdm
import torch
import torch.nn as nn

class Coach():
	def __init__(self, game, nnet, lr):
		self.game = game
		self.nnet = nnet
		self.pnet = nnet.__class__()

		self.loss = nn.MSELoss()
		self.opt = torch.optim.Adam(
			self.nnet.parameters(),
			lr=lr)

	def execute_episode(self, epsilon, gamma):
		self.game.reset()
		board = self.game.board
		## Starting color always red
		color = 'red'

		prev_state_action = {
			'red': None,
			'black': None}

		trainExamples = []
		while True:
			actions = self.game.get_possible_actions(board, color)
			state = self.game.get_state(board, color)
			state_actions = self.game.make_inputs(state, actions)
			## Epsilon greedy action selection
			out = self.nnet(state_actions)

			max_q = torch.max(out).unsqueeze(dim=0)
			max_idx = torch.argmax(out)

			if torch.rand(1) > epsilon:
				idx = max_idx
			else:
				idx = torch.randint(
					low=0,
					high=len(state_actions),
					size=(1,)).item()

			action = actions[idx]
			## Updating training examples
			if prev_state_action[color] != None:
				data = torch.cat((prev_state_action[color], gamma*max_q))
				trainExamples.append(data)
			prev_state_action[color] = state_actions[idx]
			## Executing action
			board, color = self.game.get_next_state(board, color, action)
			## If terminal state, assign rewards
			if self.game.get_game_ended(board, color):
				opponent = self.game.get_opponent_color(color)
				## Large negative reward for looser color
				data = torch.cat((prev_state_action[color], torch.tensor([-1000.0])))
				trainExamples.append(data)
				## Large positive reward for winner color
				data = torch.cat((prev_state_action[opponent], torch.tensor([1000.0])))
				trainExamples.append(data)
				break
		return trainExamples

	def learn(self, data):
		self.opt.zero_grad()
		## Strip the labels off of the last column of tensor
		X = data[:,range(data.shape[1]-1)]
		y = data[:,data.shape[1]-1].unsqueeze(dim=1)

		y_hat = self.nnet(X)
		error = self.loss(y_hat, y)
		error.backward()
		self.opt.step()
		return error.item()