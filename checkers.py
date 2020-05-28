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
		## Array representing board
		self.board = None
		## List of positions of each peice
		self.red = []
		self.black = []
		self.reset()

	## Initialize empty board
	def set_board(self):
		self.board = np.zeros((SIZE, SIZE))

	## Places peices on board
	def place_peices(self):
		## place red
		for y in range(0, 3):
			for x in range(SIZE):
				if (x + y)%2 == 0:
					self.board[y,x] = 1
		## place black
		for y in range(5, SIZE):
			for x in range(SIZE):
				if (x + y)%2 == 0:
					self.board[y,x] = -1

	## Generates list of tuples for each peice position of 
	# each color
	def get_peices_position(self):
		self.red = []
		self.black = []
		for y in range(SIZE):
			for x in range(SIZE):
				if self.board[y, x] == 1:
					self.red.append((y, x))
				elif self.board[y, x] == -1:
					self.black.append((y, x))
				else:
					pass

	def reset(self):
		self.set_board()
		self.place_peices()
		self.get_peices_position()

	## Takes int position on board
	## Returns (y, x) coordinate
	def int_to_coord(self, pos):
		return int(pos/SIZE), pos%SIZE

	## Takes coodinate tuple
	## Returns int position
	def coord_to_int(self, coord):
		return coord[0] * SIZE + coord[1]

	## Takes a peice from start_pos (int)
	## Moves it to end_pos (int)
	## Returns reward
	def move(self, color, start_pos, end_pos):
		start_coord = self.int_to_coord(start_pos)
		end_coord = self.int_to_coord(end_pos)

		peice = self.board[start_coord]
		self.board[start_coord] = 0
		self.board[end_coord] = peice

		if color == 'red':
			idx = self.red.index(start_coord)
			self.red[idx] = end_coord

		if color == 'black':
			idx = self.black.index(start_coord)
			self.black[idx] = end_coord

	def get_possible_moves(self, color):
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