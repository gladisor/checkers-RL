import numpy as np

## Board size is an 8 * 8 grid
SIZE = 8

"""
[[ 1.  0.  1.  0.  1.  0.  1.  0.]
 [ 0.  1.  0.  1.  0.  1.  0.  1.]
 [ 1.  0.  1.  0.  1.  0.  1.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0. -1.  0. -1.  0. -1.  0. -1.]
 [-1.  0. -1.  0. -1.  0. -1.  0.]
 [ 0. -1.  0. -1.  0. -1.  0. -1.]]
 """

CAPTURE_REWARD = 1

mark = {
	'red':1,
	'black':-1}

class Checkers():
	def __init__(self):
		## Array representing board
		self.board = None
		## List of positions of each peice
		self.red = []
		self.black = []

	## Initialize empty board
	def set_board(self):
		self.board = np.zeros((SIZE, SIZE))

	## Places peices on board
	def place_peices(self):
		## place red
		for y in range(0, 3):
			for x in range(SIZE):
				if (x + y)%2 == 0:
					self.board[y, x] = mark['red']
		## place black
		for y in range(5, SIZE):
			for x in range(SIZE):
				if (x + y)%2 == 0:
					self.board[y, x] = mark['black']

	## Generates list of tuples for each peice position of 
	# each color
	def get_peices_position(self):
		self.red = []
		self.black = []
		for y in range(SIZE):
			for x in range(SIZE):
				if self.board[y, x] == mark['red']:
					self.red.append((y, x))
				elif self.board[y, x] == mark['black']:
					self.black.append((y, x))
				else:
					pass

	## Re makes board
	## Places peices in correct starting position
	## Generates list of positions of each color peice
	def reset(self):
		self.set_board()
		self.place_peices()
		self.get_peices_position()
		return self.board.flatten()

	def coord_to_vect(self, coord):
		y = np.zeros(SIZE)
		y[coord[0]] = 1
		x = np.zeros(SIZE)
		x[coord[1]] = 1
		final = np.concatenate((y, x))
		return final

	def action_to_vect(self, action):
		start = self.coord_to_vect(action[0])
		end = self.coord_to_vect(action[1])
		final = np.concatenate((start, end))
		return final

	## Takes two coordinates
	## Returns midpoint
	def midpoint(self, coord1, coord2):
		y_diff = int(abs(coord1[0] + coord2[0])/2)
		x_diff = int(abs(coord1[1] + coord2[1])/2)
		return (y_diff, x_diff)

	def was_capture(self, start_coord, end_coord):
		y_diff = abs(start_coord[0] - end_coord[0])
		x_diff = abs(start_coord[1] - end_coord[1])
		if y_diff > 1 or x_diff > 1:
			return True
		return False

	def capture(self, color, start_coord, end_coord, midpoint):
		midpoint_peice = self.board[midpoint]
		self.board[midpoint] = 0
		if color == 'red':
			idx = self.black.index(midpoint)
			self.black.pop(idx)
		elif color == 'black':
			idx = self.red.index(midpoint)
			self.red.pop(idx)
		return CAPTURE_REWARD

	## Takes a peice from start_pos (int)
	## Moves it to end_pos (int)
	## Returns reward
	def move(self, color, start_coord, end_coord):
		midpoint = self.midpoint(start_coord, end_coord)

		## Move peice
		peice = self.board[start_coord]
		self.board[start_coord] = 0
		self.board[end_coord] = peice

		## Update position in list
		if color == 'red':
			idx = self.red.index(start_coord)
			self.red[idx] = end_coord
		elif color == 'black':
			idx = self.black.index(start_coord)
			self.black[idx] = end_coord

		## If move resulted in a capture, update list and return reward
		reward = 0
		if self.was_capture(start_coord, end_coord):
			reward = self.capture(color, start_coord, end_coord, midpoint)
		return reward

	## Generates and returns possible next move
	# for specified color
	def get_possible_actions(self, color):
		if color == 'red':
			peices = self.red
		elif color == 'black':
			peices = self.black

		for peice in peices:
			print(peice)

	## Takes in color, action: string, (peice at position, position to move to)
	## Executes action
	## Returns next_state, reward for each player, done (np.array, int, bool)
	def step(self, color, action):
		reward = self.move(color, action[0], action[1])
		done = False
		state = self.board
		return state, reward, done

if __name__ == "__main__":
	env = Checkers()
	state = env.reset()
	env.get_possible_actions('black')

	## Uncomment to test step function
	# players = ['red', 'black']
	# print(env.board)
	# done = False
	# while not done:
	# 	for player in players:
	# 		print(f"{player}'s turn!")
	# 		start_y = int(input("Enter y coord of peice: "))
	# 		start_x = int(input("Enter x coord of peice: "))
	# 		end_y = int(input("Enter y coord of loc: "))
	# 		end_x = int(input("Enter x coord of loc: "))

	# 		start_coord = (start_y, start_x)
	# 		end_coord = (end_y, end_x)

	# 		action = (start_coord, end_coord)

	# 		env.step(player, action)
	# 		print(env.board)

	## Uncomment this block to test move function
	# Testing functions:
	# print(env.board)
	# env.move('red', (2, 0), (3, 1))
	# print(env.board)
	# env.move('black', (5, 1), (4, 2))
	# print(env.board)
	# env.move('red', (2, 4), (3, 5))
	# print(env.board)
	# env.move('black', (4, 2), (2, 0))
	# print(env.board)
	# env.move('red', (2, 2), (3, 1))
	# print(env.board)
	# env.move('black', (5, 3), (4, 2))
	# print(env.board)
	# env.move('red', (3, 1), (5, 3))
	# print(env.board)