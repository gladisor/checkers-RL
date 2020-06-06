from game import Checkers
from tqdm import tqdm
import numpy as np

class Arena():
	def __init__(self, player1, player2, game):
		self.player1 = player1
		self.player2 = player2
		self.game = game

	def play_game(self, epsilon=0, display=False):
		players = {
			'red':self.player1,
			'black':self.player2}

		self.game.reset()
		board = self.game.board
		color = 'red'
		while not self.game.get_game_ended(board, color):
			actions = self.game.get_possible_actions(board, color)
			state = self.game.get_state(board, color)
			state_actions = self.game.make_inputs(state, actions)
			if np.random.rand() > epsilon:
				idx = players[color](state_actions)
			else:
				idx = np.random.randint(len(actions))
			action = actions[idx]
			board, color = self.game.get_next_state(board, color, action)
			if display:
				print(board)
				print(f"Action: {action}")
		return color