from game import Checkers
from dqn import DQN
from agent import Agent
from arena import Arena
from tqdm import tqdm
import torch
import torch.nn as nn
import numpy as np

class Coach():
	def __init__(self, game, nnet):
		self.game = game
		self.nnet = nnet
		self.pnet = nnet.__class__()
		self.trainExamplesHistory = []

	def execute_episode(self, epsilon=0.3, gamma=0.80):
		self.game.reset()
		board = self.game.board
		## Starting color always red
		color = 'red'

		agent = Agent(self.nnet, epsilon)

		prev_state_action = {
			'red':None,
			'black':None}

		X = []
		target = []
		while True:
			actions = self.game.get_possible_actions(board, color)
			state = self.game.get_state(board, color)
			state_actions = self.game.make_inputs(state, actions)
			## Epsilon greedy action selection
			idx = agent.choose_action_egreedy(state_actions)
			action = actions[idx]
			## Updating training examples
			if prev_state_action[color] != None:
				max_q = torch.max(self.nnet(state_actions)).item()
				X.append(prev_state_action[color])
				target.append(gamma*max_q)
			prev_state_action[color] = state_actions[idx]
			## Executing action
			board, color = self.game.get_next_state(board, color, action)
			## If terminal state, assign rewards
			if self.game.get_game_ended(board, color):
				opponent = self.game.get_opponent_color(color)
				X.append(prev_state_action[color])
				target.append(-1000)
				X.append(prev_state_action[opponent])
				target.append(1000)
				X = torch.stack(X)
				target = torch.tensor(target)
				target = target.unsqueeze(1)
				break
		return X, target


if __name__ == "__main__":
	game = Checkers()
	## Network to be trained using coach
	dqn = DQN()

	coach = Coach(
		game=game,
		nnet=dqn)

	PATH = "models/testmodel.pt"

	for epoch in range(5):
		torch.save(coach.nnet.state_dict(), PATH)
		coach.pnet.load_state_dict(torch.load(PATH))

		for _ in tqdm(range(50), desc="Self play"):
			X, target = coach.execute_episode()
			loss = nn.MSELoss()
			opt = torch.optim.Adam(coach.nnet.parameters(), lr=0.0001)

			opt.zero_grad()
			out = coach.nnet(X)
			error = loss(out, target)
			error.backward()
			opt.step()
			
		X, target = coach.execute_episode(
			epsilon=0.3,
			gamma=0.95)

		arena = Arena(
			player1=lambda x: torch.argmax(coach.nnet(x)),
			player2=lambda x: torch.argmax(coach.pnet(x)),
			game=coach.game)

		nwins, pwins = arena.play_games(10)

		if float(nwins)/(nwins+pwins) >= 0.5:
			torch.save(coach.nnet.state_dict(), PATH)
		else:
			coach.nnet.load_state_dict(torch.load(PATH))
		print(nwins, pwins)