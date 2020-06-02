import numpy as np

## Board size is an 8 * 8 grid
SIZE = 8

"""
   0  1  2  3  4  5  6  7  
0 [1. 0. 1. 0. 1. 0. 1. 0.]
1 [0. 1. 0. 1. 0. 1. 0. 1.]
2 [1. 0. 1. 0. 1. 0. 1. 0.]
3 [0. 0. 0. 0. 0. 0. 0. 0.]
4 [0. 0. 0. 0. 0. 0. 0. 0.]
5 [0. 2. 0. 2. 0. 2. 0. 2.]
6 [2. 0. 2. 0. 2. 0. 2. 0.]
7 [0. 2. 0. 2. 0. 2. 0. 2.]
 """
mark = {
	'red':1,
	'black':-1}

class Checkers():
	"""
	Class that simulates checkers games and also
	serves as the backend for the GUI
	"""
	def __init__(self, starting='red'):
		## Array representing board
		self.board = None
		self.selfPlay = True

	def set_board(self):
		"""
		Returns:
			8x8 numpy array of zeros
		"""
		return np.zeros((SIZE, SIZE))

	def place_pieces(self, board):
		"""
		Inputs:
			8x8 numpy array
		"""
		## place red
		for y in range(0, 3):
			for x in range(SIZE):
				if (x + y)%2 == 0:
					board[y, x] = mark['red']
		## place black
		for y in range(5, SIZE):
			for x in range(SIZE):
				if (x + y)%2 == 0:
					board[y, x] = mark['black']

	def reset(self):
		"""
		Re makes board
		Places pieces in correct starting position
		Generates list of positions of each color piece
		"""
		self.board = self.set_board()
		self.place_pieces(self.board)

	def get_state(self, board, color):
		"""
		Inputs:
			numpy array 8x8,
			color string of current player
		Returns:
			Flattened array, normalized to be standard
			with respect to each player
		"""
		if color == 'red':
			return board.flatten()
		elif color == 'black':
			return -1*np.rot90(board, 2).flatten()

	def midpoint(self, coord1, coord2):
		"""
		Inputs:
			Starting and ending coordinates
		Returns:
			Midpoint between two coords.
		"""
		y_diff = int(abs(coord1[0] + coord2[0])/2)
		x_diff = int(abs(coord1[1] + coord2[1])/2)
		return (y_diff, x_diff)

	def get_next_state(self, board, color, action):
		"""
		Inputs:
			8x8 board,
			String color of current player,
			Coord representation of action
		Returns:
			Board,
			Next player color
		"""
		startCoord = action[0]
		endCoord = action[1]

		piece = board[startCoord]
		board[startCoord] = 0
		board[endCoord] = piece

		## Condition to handle if move was a capture
		hasNextMove = False
		y_diff = abs(startCoord[0] - endCoord[0])
		x_diff = abs(startCoord[1] - endCoord[1])
		if y_diff > 1 and x_diff > 1:
			midpoint = self.midpoint(startCoord, endCoord)
			midpoint_piece = self.board[midpoint]
			board[midpoint] = 0
			hasNextMove = True

		if hasNextMove:
			next_color = color
		else:
			next_color = self.get_opponent_color(color)
		return board, next_color

	def get_piece_positions(self, board, color):
		"""
		Inputs:
			board 8x8,
			string color
		Returns:
			list of current position of all pieces of that color
		"""
		positions = []
		for y in range(SIZE):
			for x in range(SIZE):
				if self.board[y, x] == mark[color]:
					positions.append((y, x))
		return positions

	def within_bounds(self, coord):
		"""
		Checks if piece is within bounds
		"""
		if 0 <= coord[0] < SIZE and 0 <= coord[1] < SIZE:
			withinBounds = True
		else:
			withinBounds = False
		return withinBounds

	def get_opponent_color(self, color):
		"""
		Returns opponent color
		"""
		if color == 'red':
			return 'black'
		else:
			return 'red'

	def get_piece_actions(self, color, piece):
		"""
		Takes String color, and coordinate of piece
		Checks 4 possible moves
		Returns valid actions for that piece
		"""
		if color == 'red':
			forward_move = 1
			forward_jump = 2
		else:
			forward_move = -1
			forward_jump = -2
		## Normal moves
		left_move = (piece[0] + forward_move, piece[1] + 1)
		right_move = (piece[0] + forward_move, piece[1] - 1)
		## Capture moves
		left_jump = (piece[0] + forward_jump, piece[1] + 2)
		right_jump = (piece[0] + forward_jump, piece[1] - 2)

		left_midpoint = self.midpoint(piece, left_jump)
		right_midpoint = self.midpoint(piece, right_jump)
		opponent_color = self.get_opponent_color(color)

		possible_actions = []
		## Check if left move is valid
		if self.within_bounds(left_move) and self.board[left_move] == 0:
			possible_actions.append((piece, left_move))
		## Check if right move is valid
		if self.within_bounds(right_move) and self.board[right_move] == 0:
			possible_actions.append((piece, right_move))
		## Check if left jump is valid
		if self.within_bounds(left_jump) and self.board[left_jump] == 0 \
				and self.board[left_midpoint] == mark[opponent_color]:
			possible_actions.append((piece, left_jump))
		## Check if right jump is valid
		if self.within_bounds(right_jump) and self.board[right_jump] == 0 \
				and self.board[right_midpoint] == mark[opponent_color]:
			possible_actions.append((piece, right_jump))
		return possible_actions

	def flip_coord(self, coord):
		"""
		Takes in coordinate tuple (y, x)
		Returns coordinate from the perspective of the other side
		"""
		coord = (abs(coord[0] - SIZE + 1), abs(coord[1] - SIZE + 1))
		return coord

	def flip_action(self, action):
		"""
		Takes action tuple (start_coord, end_coord)
		Flips start and end coord
		"""
		action = (self.flip_coord(action[0]), self.flip_coord(action[1]))
		return action

	def get_possible_actions(self, board, color):
		"""
		Inputs:
			board 8x8,
			string color
		Returns:
			list of possible actions
		"""
		pieces = self.get_piece_positions(board, color)

		possible_actions = []
		for piece in pieces:
			possible_actions.extend(self.get_piece_actions(color, piece))

		if self.selfPlay == True and color == 'black':
			for i in range(len(possible_actions)):
				possible_actions[i] = self.flip_action(possible_actions[i])

		return possible_actions

	def get_game_ended(self, board, color):
		if not self.get_possible_actions(board, color):
			terminal = True
		else:
			terminal = False
		return terminal

	def render(self):
		"""
		Primative display function
		"""
		print(self.board)

	def coord_to_vect(self, coord):
		"""
		Takes (y, x) coord
		Returns onehot encoded vector representation
		"""
		y = np.zeros(SIZE)
		y[coord[0]] = 1
		x = np.zeros(SIZE)
		x[coord[1]] = 1
		final = np.concatenate((y, x))
		return final

	def action_to_vect(self, action):
		"""
		Converts action tuple of the form: (start_coord, end_coord)
		Returns onehot vector representation of that action
		"""
		start = self.coord_to_vect(action[0])
		end = self.coord_to_vect(action[1])
		final = np.concatenate((start, end))
		return final


if __name__ == "__main__":
	env = Checkers()
	env.reset()
	env.selfPlay = False
	color = 'red'

	board = env.board
	print(board)
	while not env.get_game_ended(board, color):
		actions = env.get_possible_actions(board, color)
		idx = np.random.choice(range(len(actions)))
		action = actions[idx]
		print(f"{color}'s turn")
		print(f"{color}'s action: {action}")
		board, color = env.get_next_state(board, color, action)
		print(board)
	print(f"{color} has no moves!")
