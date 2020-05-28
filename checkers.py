import numpy as np

SIZE = 8

class Checkers():
	def __init__(self):
		self.board = self.set_board()
		self.place_peices()

	def set_board(self):
		return np.zeros((SIZE, SIZE))

	def place_peices(self):
		## place white
		for y in range(0, 3):
			for x in range(SIZE):
				if (x + y)%2 == 0:
					self.board[y,x] = 1
		## place black
		for y in range(5, SIZE):
			for x in range(SIZE):
				if (x + y)%2 == 0:
					self.board[y,x] = -1

	def get_possible_moves(self):
		raise NotImplementedError

	def render(self):
		raise NotImplementedError

	def reset(self):
		raise NotImplementedError

	def close(self):
		raise NotImplementedError

	def step(self, action):
		raise NotImplementedError

if __name__ == "__main__":
	env = Checkers()
	print(env.board.flatten())