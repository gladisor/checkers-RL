from game import Checkers
from dqn import DQN
from arena import Arena
from tqdm import tqdm
import torch
import torch.nn as nn

class Coach():
	def __init__(self, game, nnet):
		self.game = game
		self.nnet = nnet
		self.pnet = nnet.__class__()
		self.trainExamplesHistory = []

	def execute_episode(self, epsilon, gamma):
		self.game.reset()
		board = self.game.board
		## Starting color always red
		color = 'red'

		prev_state_action = {
			'red': None,
			'black': None}

		trainExamples = []
		while True:
			actions = self.game.get_possible_actions(board, color)
			state = self.game.get_state(board, color)
			state_actions = self.game.make_inputs(state, actions)
			## Epsilon greedy action selection
			out = self.nnet(state_actions)

			max_q = torch.max(out).unsqueeze(dim=0)
			max_idx = torch.argmax(out)

			if torch.rand(1) > epsilon:
				idx = max_idx
			else:
				idx = torch.randint(
					low=0,
					high=len(state_actions),
					size=(1,)).item()

			action = actions[idx]
			## Updating training examples
			if prev_state_action[color] != None:
				data = torch.cat((prev_state_action[color], gamma*max_q))
				trainExamples.append(data)
			prev_state_action[color] = state_actions[idx]
			## Executing action
			board, color = self.game.get_next_state(board, color, action)
			## If terminal state, assign rewards
			if self.game.get_game_ended(board, color):
				opponent = self.game.get_opponent_color(color)
				## Large negative reward for looser color
				data = torch.cat((prev_state_action[color], torch.tensor([-1000.0])))
				trainExamples.append(data)
				## Large positive reward for winner color
				data = torch.cat((prev_state_action[opponent], torch.tensor([1000.0])))
				trainExamples.append(data)
				break
		return trainExamples


if __name__ == "__main__":
	# torch.set_printoptions(profile="short", sci_mode=False)
	game = Checkers()
	## Network to be trained using coach
	dqn = DQN()

	coach = Coach(
		game=game,
		nnet=dqn)

	loss = nn.MSELoss()
	opt = torch.optim.Adam(coach.nnet.parameters(), lr=0.0001)

	PATH = "models/test.pt"

	num_improvements = 0
	for _ in range(80):
		torch.save(coach.nnet.state_dict(), PATH)
		coach.pnet.load_state_dict(torch.load(PATH))

		for episode in tqdm(range(100), desc="Training"):
			data = coach.execute_episode(
				epsilon=0.3,
				gamma=0.80)

			data = torch.stack(data)
			X = data[:,range(data.shape[1]-1)]
			y = data[:,data.shape[1]-1].unsqueeze(dim=1)

			opt.zero_grad()
			y_hat = coach.nnet(X)
			error = loss(y_hat, y)
			error.backward()
			opt.step()

		arena = Arena(
			player1=lambda x: torch.argmax(coach.nnet(x)),
			player2=lambda x: torch.argmax(coach.pnet(x)),
			game=game)

		p1_won = 0
		p2_won = 0

		result = arena.play_game()
		if result == 'red':
			p2_won += 1
		else:
			p1_won += 1

		arena.player1, arena.player2 = arena.player2, arena.player1

		result = arena.play_game()
		if result == 'red':
			p1_won += 1
		else:
			p2_won += 1

		if p1_won > p2_won:
			print("Accepting model :D")
			torch.save(coach.nnet.state_dict(), PATH)
			num_improvements += 1
		else:
			print("Rejecting model :(")
			coach.nnet.load_state_dict(torch.load(PATH))

		print(f"Agent wins: {p1_won}, Prev agent wins {p2_won}, Improvements {num_improvements}")