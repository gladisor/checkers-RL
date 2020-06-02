from dqn import DQN
from game import Checkers
import torch
import numpy as np

class Arena():
	def __init__(self, player1, player2, game):
		"""
		Inputs:
			player1, lambda function which selects action given state
			player2, same as player 1
			game, Environment to play agents against each other
		"""
		self.player1 =  player1
		self.player2 = player2
		self.game = game

	def make_inputs(self, state, actions):
		state = torch.tensor(state)

		X = []
		for action in actions:
			action_vect = env.action_to_vect(action)
			action_vect = torch.tensor(action_vect)
			vect = torch.cat((state, action_vect))
			X.append(vect)
		X = torch.stack(X).float()
		return X

	def playGame(self, display=False):
		players = {
			'red': self.player1,
			'black': self.player2}

		self.game.reset()
		count = 0
		turn = 0
		curColor = list(players.keys())[count]
		board = self.game.board
		while not self.game.get_game_ended(board, curColor):
			self.game.get_game_ended(board, curColor)
			turn += 1
			## Get state and possible actions
			state = self.game.get_state(board, curColor)
			actions = self.game.get_possible_actions(board, curColor)
			## Action selection
			stateActions = self.make_inputs(state, actions)
			idx = players[curColor](stateActions)
			action = actions[idx]
			## If action was from black perspective: filp.
			if curColor == 'black':
				action = self.game.flip_action(action)
			## Execute action
			prevColor = curColor
			board, curColor = self.game.get_next_state(board, curColor, action)
			count = (count + 1) % 2
			## Print results
			if display:
				print(f"{prevColor}'s -> turn: {turn} action: {action}")
				print(board)
		return curColor

if __name__ == "__main__":	
	dqn = DQN(
		d_in=96,
		d_hidden=64,
		num_hidden=3).float()

	env = Checkers()

	arena = Arena(
		player1=lambda x: torch.argmax(dqn(x)),
		player2=lambda x: torch.argmax(dqn(x)),
		game=env)

	result = arena.playGame(display=True)
	print(f"{result} lost")

