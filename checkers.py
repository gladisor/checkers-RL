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
	"""
	Class that simulates checkers games and also
	serves as the backend for the GUI
	"""
	def __init__(self):
		## Array representing board
		self.board = None
		## Bit representing position of board:
		# 0 is standard
		# 1 is flipped
		## This allows the agent to play against itself
		self.board_direction = None
		## List of positions of each piece
		self.pieces = {
			'red':[],
			'black':[]}

		self.selfPlay = True

	def set_board(self):
		"""
		Initialize empty board
		"""
		self.board = np.zeros((SIZE, SIZE))

	
	def place_pieces(self):
		"""
		Places pieces on board
		Records position in lists
		"""
		## place red
		for y in range(0, 3):
			for x in range(SIZE):
				if (x + y)%2 == 0:
					self.board[y, x] = mark['red']
					self.pieces['red'].append((y, x))
		## place black
		for y in range(5, SIZE):
			for x in range(SIZE):
				if (x + y)%2 == 0:
					self.board[y, x] = mark['black']
					self.pieces['black'].append((y, x))

	def reset(self):
		"""
		Re makes board
		Places pieces in correct starting position
		Generates list of positions of each color piece
		"""
		self.set_board()
		self.place_pieces()
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

	def capture(self, opponent_color, start_coord, end_coord):
		"""
		Removes captured piece from board
		Pops captured piece from opponent pieces
		"""
		midpoint = self.midpoint(start_coord, end_coord)
		midpoint_piece = self.board[midpoint]
		self.board[midpoint] = 0
		idx = self.pieces[opponent_color].index(midpoint)
		self.pieces[opponent_color].pop(idx)

	def get_opponent_color(self, color):
		if color == 'red':
			return 'black'
		else:
			return 'red'

	def move(self, color, start_coord, end_coord):
		"""
		Takes a piece from start_pos (int)
		Moves it to end_pos (int)
		Returns reward
		"""
		## Move piece
		piece = self.board[start_coord]
		self.board[start_coord] = 0
		self.board[end_coord] = piece

		## Update position in list
		idx = self.pieces[color].index(start_coord)
		self.pieces[color][idx] = end_coord

		## If move resulted in a capture, update list and return reward
		has_next_move = False
		reward = 0
		if self.was_capture(start_coord, end_coord):
			opponent_color = self.get_opponent_color(color)
			self.capture(opponent_color, start_coord, end_coord)
			reward += CAPTURE_REWARD
			has_next_move = True
		return reward, has_next_move

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

	def get_cannonical_board(self, color):
		"""
		Takes string color
		Returns board from standardized perspective
		"""
		if color == 'red':
			return self.board.flatten()
		elif color == 'black':
			return np.rot90(self.board, 2).flatten()

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
		left_move = (piece[0] + forward_move, piece[1] + 1)
		right_move = (piece[0] + forward_move, piece[1] - 1)
		left_jump = (piece[0] + forward_jump, piece[1] + 2)
		right_jump = (piece[0] + forward_jump, piece[1] - 2)

		left_midpoint = self.midpoint(piece, left_jump)
		right_midpoint = self.midpoint(piece, right_jump)
		opponent_color = self.get_opponent_color(color)

		possible_actions = []
		if self.within_bounds(left_move) and self.board[left_move] == 0:
			possible_actions.append((piece, left_move))
		if self.within_bounds(right_move) and self.board[right_move] == 0:
			possible_actions.append((piece, right_move))
		if self.within_bounds(left_jump) and self.board[left_jump] == 0 \
				and self.board[left_midpoint] == opponent_color:
			possible_actions.append((piece, left_jump))
		if self.within_bounds(right_jump) and self.board[right_jump] == 0 \
				and self.board[right_midpoint] == opponent_color:
			possible_actions.append((piece, right_jump))
		return possible_actions

	def get_possible_actions(self, color):
		"""
		Generates and returns possible next move
		for specified color
		"""
		possible_actions = []
		for piece in self.pieces[color]:
			possible_actions.extend(self.get_piece_actions(color, piece))
		return possible_actions

	def win_condition(self, color):
		if not self.get_possible_actions(self.get_opponent_color(color)):
			terminal = True
		else:
			terminal = False
		return terminal

	def step(self, color, action):
		"""
		Takes in color, action: string, (start_coord, end_coord)
		Executes action
		Returns next_state, reward for each player, terminal (np.array, int, bool)
		"""

		## Flip the action perspective if agent is playing another agent
		if color == 'black' and self.selfPlay == True:
			action = self.flip_action(action)

		reward, has_next_move = self.move(color, action[0], action[1])
		terminal = self.win_condition(color)

		## If the current color has a next move 
		# return the board as it was before
		# otherwise return the board from opponents perspective
		if has_next_move:
			state = self.get_cannonical_board(color)
		else:
			opponent_color = self.get_opponent_color(color)
			state = self.get_cannonical_board(opponent_color)
		return state, reward, terminal, has_next_move

	def render(self):
		"""
		Primative display function with indexes, neutral perspective
		"""
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
	env.selfPlay = False

	## Test loop
	terminal = False
	while not terminal:
		for color in mark.keys():
			has_next_move = True
			while has_next_move:
				possible_actions = env.get_possible_actions(color)
				if not possible_actions:
					break

				idx = np.random.choice(range(len(possible_actions)))
				action = possible_actions[idx]
				state, reward, terminal, has_next_move = env.step(color, action)
				
				print()
				print(f"Action: {action}")
				print(f"{color}'s move")
				print(f"Terminal? {terminal}")
				print()
				env.render()
				if terminal:
					break
		