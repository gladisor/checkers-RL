import numpy as np

### NOTE: remove red black functionality for move
## selection. Replace with flipping board

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
	'black':2}

class Checkers():
	def __init__(self):
		## Array representing board
		self.board = None
		## Bit representing position of board:
		# 0 is standard
		# 1 is flipped
		## This allows the agent to play against itself
		self.board_direction = None
		## List of positions of each peice
		self.pieces = {
			'red':[],
			'black':[]}

	## Initialize empty board
	def set_board(self):
		self.board = np.zeros((SIZE, SIZE))

	## Places pieces on board
	def place_pieces(self):
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
	def get_pieces_position(self):
		self.pieces['red'] = []
		self.pieces['black'] = []

		for y in range(SIZE):
			for x in range(SIZE):
				if self.board[y, x] == mark['red']:
					self.pieces['red'].append((y, x))
				elif self.board[y, x] == mark['black']:
					self.pieces['black'].append((y, x))
				else:
					pass

	## Re makes board
	## Places pieces in correct starting position
	## Generates list of positions of each color peice
	def reset(self):
		self.set_board()
		self.place_pieces()
		self.get_pieces_position()
		self.board_direction = 0
		return self.board.flatten()

	## Takes (y, x) coord
	## Returns onehot encoded vector representation
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
		if y_diff > 1 and x_diff > 1:
			return True
		return False

	## Removes captured piece from board
	## Pops captured piece from opponent pieces
	def capture(self, opponent_color, start_coord, end_coord, midpoint):
		midpoint_piece = self.board[midpoint]
		self.board[midpoint] = 0
		idx = self.pieces[opponent_color].index(midpoint)
		self.pieces[opponent_color].pop(idx)

	## Takes a piece from start_pos (int)
	## Moves it to end_pos (int)
	## Returns reward
	def move(self, color, start_coord, end_coord):
		midpoint = self.midpoint(start_coord, end_coord)

		## Move peice
		piece = self.board[start_coord]
		self.board[start_coord] = 0
		self.board[end_coord] = piece

		## Update position in list
		idx = self.pieces[color].index(start_coord)
		self.pieces[color][idx] = end_coord

		## If move resulted in a capture, update list and return reward
		reward = 0
		if self.was_capture(start_coord, end_coord):
			if color == 'red':
				opponent_color = 'black'
			elif color == 'black':
				opponent_color = 'red'
			self.capture(opponent_color, start_coord, end_coord, midpoint)
			reward += CAPTURE_REWARD
		return reward

	def flip_coord(self, coord):
		coord = (abs(coord[0] - SIZE + 1), abs(coord[1] - SIZE + 1))
		return coord

	def flip_board(self):
		self.board = np.rot90(self.board, 2)
		for key in self.pieces.keys():
			for i in range(len(self.pieces[key])):
				self.pieces[key][i] = self.flip_coord(self.pieces[key][i])

		## Alternates this variable 0-1-0-1...
		self.board_direction = (self.board_direction + 1)%2

	def get_pieces_moves(self, color, piece, board_direction):
		return

	## Generates and returns possible next move
	# for specified color
	def get_possible_actions(self, color):
		return

	def win_condition(self):
		return

	## Takes in color, action: string, (piece at position, position to move to)
	## Executes action
	## Returns next_state, reward for each player, done (np.array, int, bool)
	def step(self, color, action):
		reward = self.move(color, action[0], action[1])
		done = False
		state = self.board
		return state, reward, done

	## Primative display function with indexes
	def render(self):
		print("  ", end=" ")
		for i in range(8):
			print(i, end="  ")
		print()

		for idx, row in enumerate(env.board):
			print(idx, row)

if __name__ == "__main__":
	env = Checkers()
	state = env.reset()
	env.render()

	## Test loop
	done = False
	while not done:
		for color in mark.keys():
			print(f"{color}'s turn")
			start_y = int(input("start y: "))
			start_x = int(input("start x: "))
			end_y = int(input("end y: "))
			end_x = int(input("end x: "))
			action = ((start_y, start_x), (end_y, end_x))
			env.step(color, action)
			env.flip_board()
			env.render()
		