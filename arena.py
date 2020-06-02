from dqn import DQN
from checkers import Checkers

class Arena():
	def __init__(self, player1, player2, game):
		self.player1 =  player1
		self.player2 = player2
		self.game = game

	def playGame(self):
		players = {
			'red': self.player1,
			'black': self.player2}

		self.game.reset()
		count = 0
		curColor = list(players.keys())[count]
		while self.game.get_game_ended(self.game.board, curColor):
			state = self.game.get_board(board, curColor)
			actions = self.game.get_possible_actions(self.game.board, curColor)
			action = players[curColor].select_action(state, actions)
		count = (count + 1) % 2

if __name__ == "__main__":
	players = {
		'red': 5,
		'black': 6}

	print(list(players.keys())[0])