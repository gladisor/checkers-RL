from game import Checkers
from dqn import DQN
from agent import Agent
import torch
import numpy as np

class Coach():
	def __init__(self, game, nnet):
		self.game = game
		self.nnet = nnet
		self.pnet = nnet.__class__()
		self.trainExamplesHistory = []

	def execute_episode(self, epsilon=0.3, gamma=0.80):
		trainExamples = []

		self.game.reset()
		board = self.game.board
		color = 'red'

		agent = Agent(self.nnet, epsilon)

		prev_state_action = {
			'red':None,
			'black':None}
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
				trainExamples.append([prev_state_action[color], gamma*max_q])
			prev_state_action[color] = state_actions[idx]
			board, color = self.game.get_next_state(board, color, action)
			if self.game.get_game_ended(board, color):
				opponent = self.game.get_opponent_color(color)
				trainExamples.append([prev_state_action[color], -100])
				trainExamples.append([prev_state_action[opponent], 100])
				break
		return trainExamples


if __name__ == "__main__":
	game = Checkers()
	dqn = DQN()

	coach = Coach(
		game=game,
		nnet=dqn)

	data = coach.execute_episode()
	print(data)