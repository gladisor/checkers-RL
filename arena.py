from game import Checkers
from dqn import DQN
from agent import Agent
from tqdm import tqdm

class Arena():
	def __init__(self, player1, player2, game):
		self.player1 = player1
		self.player2 = player2
		self.game = game

	def play_game(self, display=False):
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
			idx = players[color](state_actions)
			action = actions[idx]
			board, color = self.game.get_next_state(board, color, action)
			if display:
				print(board)
		return color

if __name__ == "__main__":
	nnet = Agent(epsilon=0.5)
	pnet = Agent(epsilon=0.5)

	game = Checkers()

	arena = Arena(
		player1=lambda x: nnet.choose_action_egreedy(x),
		player2=lambda x: pnet.choose_action_egreedy(x),
		game=game)

	arena.play_game(display=True)