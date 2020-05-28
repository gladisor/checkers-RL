import numpy as np

SIZE = 8

class Checkers():
	def __init__(self):
		self.board = set_board()

	def set_board(self):
		return np.zeros((SIZE, SIZE))

	def reset(self):
		raise NotImplementedError

	def step(self, action):
		raise NotImplementedError

if __name__ == "__main__":
	env = Checkers()

	print(env.board)