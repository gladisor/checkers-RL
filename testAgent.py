from game import Checkers
from dqn import DQN

import torch

PATH = "models/30Improve.pt"
dqn = DQN()
dqn.load_state_dict(torch.load(PATH))

game = Checkers()
game.reset()

board = game.board
## Display
print(board)

color = 'red'
while not game.get_game_ended(board, color):
	actions = game.get_possible_actions(board, color)
	state = game.get_state(board, color)
	state_actions = game.make_inputs(state, actions)
	if color == 'black':
		print("Agent turn")
		print("Agent possible actions")

		out = dqn(state_actions)
		for a, q in zip(actions, out):
			print(game.flip_action(a), q.item())
		print(torch.max(out))
		idx = torch.argmax(out)
		action = actions[idx]
	else:
		print("Your turn")
		start_y = int(input("Enter start y: "))
		start_x = int(input("Enter start x: "))
		end_y = int(input("Enter end y: "))
		end_x = int(input("Enter end x: "))
		action = ((start_y, start_x), (end_y, end_x))

	board, color = game.get_next_state(board, color, action)
	## Display
	print(board)
	print()