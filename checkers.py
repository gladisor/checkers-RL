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

CAPTURE_REWARD = 1

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
		Initialize empty board
		"""
		return np.zeros((SIZE, SIZE))

	
	def place_pieces(self, board):
		"""
		Places pieces on board
		Records position in lists
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
		## Red starts first so always return standard board
		return self.board.flatten()

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

	def midpoint(self, coord1, coord2):
		"""
		Takes two coordinates
		Returns midpoint
		"""
		y_diff = int(abs(coord1[0] + coord2[0])/2)
		x_diff = int(abs(coord1[1] + coord2[1])/2)
		return (y_diff, x_diff)

	def was_capture(self, start_coord, end_coord):
		"""
		Takes two coordinates
		If the move was a capture return True
		"""
		y_diff = abs(start_coord[0] - end_coord[0])
		x_diff = abs(start_coord[1] - end_coord[1])
		if y_diff > 1 and x_diff > 1:
			return True
		return False

	def get_opponent_color(self, color):
		"""
		Returns opponent color
		"""
		if color == 'red':
			return 'black'
		else:
			return 'red'

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

	def get_state(self, board, color):
		"""
		Takes string color
		Returns board from standardized perspective
		"""
		if color == 'red':
			return board.flatten()
		elif color == 'black':
			return -1*np.rot90(board, 2).flatten()

	def within_bounds(self, coord):
		"""
		Checks if piece is within bounds
		"""
		if 0 <= coord[0] < SIZE and 0 <= coord[1] < SIZE:
			withinBounds = True
		else:
			withinBounds = False
		return withinBounds

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

	def get_piece_positions(self, board, color):
		"""
		Returns a list of current position of all pieces of that color
		"""
		positions = []
		for y in range(SIZE):
			for x in range(SIZE):
				if self.board[y, x] == mark[color]:
					positions.append((y, x))
		return positions

	def get_possible_actions(self, board, color):
		"""
		Generates and yeah probably I do need reassurance like I'm very nice I need yeah so you're not like mad at me or anything and Erin's not mad at me or I don't know I just have that feeling sometimes I guess it's just yeah allreturns possible next move
		for specified color
		"""
		pieces = self.get_piece_positions(board, color)

		possible_actions = []
		for piece in pieces:
			possible_actions.extend(self.get_piece_actions(color, piece))

		if self.selfPlay == True:
			for i in range(len(possible_actions)):
				possible_actions[i] = self.flip_action(possible_actions[i])

		return possible_actions

	def win_condition(self, board, color):
		## If opponent has no moves, you won
		if not self.get_possible_actions(board, self.get_opponent_color(color)):
			terminal = True
		else:
			terminal = False
		return terminal

	def get_game_ended(self, board, color):
		if not self.get_possible_actions(board, color):
			terminal = True
		else:
			terminal = False
		return terminal

	def move(self, board, color, start_coord, end_coord):
		"""
		Takes a piece from start_pos (int)
		Moves it to end_pos (int)
		Returns reward
		"""
		## Move piece
		piece = board[start_coord]
		board[start_coord] = 0
		board[end_coord] = piece

		## If move resulted in a capture, remove captured piece from board
		hasNextMove = False
		if self.was_capture(start_coord, end_coord):
			midpoint = self.midpoint(start_coord, end_coord)
			midpoint_piece = self.board[midpoint]
			board[midpoint] = 0
			hasNextMove = True
		return hasNextMove

	def step(self, board, color, action):
		"""
		Takes in color, action: string, (start_coord, end_coord)
		Executes action
		Returns next_state, reward for each player, terminal (np.array, int, bool)
		"""

		## Flip the action perspective if agent is playing another agent
		if color == 'black' and self.selfPlay == True:
			action = self.flip_action(action)

		hasNextMove = self.move(board, color, action[0], action[1])
		terminal = self.win_condition(board, color)

		reward = 0
		if terminal:
			reward = 1

		## If the current color has a next move 
		# return the board as it was before
		# otherwise return the board from opponents perspective
		if hasNextMove:
			state = self.get_state(self.board, color)
		else:
			opponent_color = self.get_opponent_color(color)
			state = self.get_state(self.board, opponent_color)
		return state, reward, terminal, hasNextMove

	def render(self):
		"""
		Primative display function
		"""
		print(self.board)

if __name__ == "__main__":
	env = Checkers()
	state = env.reset()
	env.selfPlay = False
	env.render()

	## Test loop
	terminal = False
	while not terminal:
		for color in mark.keys():
			hasNextMove = True
			while hasNextMove == True:
				possible_actions = env.get_possible_actions(env.board, color)
				if not possible_actions:
					break

				idx = np.random.choice(range(len(possible_actions)))
				action = possible_actions[idx]
				state, reward, terminal, hasNextMove = env.step(env.board, color, action)
				
				print()
				print(f"{color}'s move")
				print(f"Action: {action}")
				print(f"Terminal? {terminal}")
				print(f"{color} reward: {reward}")
				print()

				env.render()
				print(hasNextMove)
				if terminal:
					break
			if terminal:
				break
		if terminal:
			break