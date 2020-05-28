import numpy as np

SIZE = 8

## May use Peice class instead of int to represent peices
class Peice():
	def __init__(self, color, y, x, dead=False):
		self.color = color
		self.dead = dead
		self.y = y
		self.x = x
		self.crowned = False

class Checkers():
	def __init__(self):
		self.board = None
		self.reset()

	def set_board(self):
		return np.zeros((SIZE, SIZE))

	## places peices on board
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

	def reset(self):
		self.board = self.set_board()
		self.place_peices()

	## Takes int position on board
	## Returns (y, x) coordinate
	def int_to_coord(self, pos):
		return int(pos/SIZE), pos%SIZE

	## Takes a peice from start_pos (int)
	## Moves it to end_pos (int)
	## Returns reward
	def move(self, start_pos, end_pos):
		start_coord = self.int_to_coord(start_pos)
		end_pos = self.int_to_coord(end_pos)

		peice = self.board[start_coord]
		self.board[start_coord] = 0

		self.board[end_pos] = peice

	def get_possible_moves(self):
		raise NotImplementedError

	def render(self):
		raise NotImplementedError

	def close(self):
		raise NotImplementedError

	## Takes in an action (tuple)
	## Executes action
	## Returns next_state, reward, done (np.array, int, bool)
	def step(self, action):
		raise NotImplementedError

if __name__ == "__main__":
	env = Checkers()
	print(env.board)
	env.move(16, 25)
	print(env.board)