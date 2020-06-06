from dqn import DQN
from coach import Coach
from game import Checkers
from arena import Arena

import torch
from tqdm import tqdm

def get_Xy(data):
	X = data[:,range(data.shape[1]-1)]
	y = data[:,data.shape[1]-1].unsqueeze(dim=1)
	return X, y

game = Checkers()

dqn = DQN(
	d_in=68,
	d_hidden=32,
	num_hidden=5)

coach = Coach(
	game=game,
	nnet=dqn,
	lr=0.01)

PATH = "models/test.pt"
num_improvements = 0

for _ in range(80):
	## Saving a copy of the current network weights to pnet
	torch.save(coach.nnet.state_dict(), PATH)
	coach.pnet.load_state_dict(torch.load(PATH))

	for _ in tqdm(range(100), desc="Self play"):
		data = coach.execute_episode(epsilon=0.3, gamma=0.80)
		data = torch.stack(data)
		coach.learn(data)

	arena = Arena(
		player1=lambda x: torch.argmax(coach.nnet(x)),
		player2=lambda x: torch.argmax(coach.pnet(x)),
		game=game)

	## Introduce small randomness into evaluation games
	## Both agents take random moves with small probability
	p1_won = 0
	p2_won = 0
	for _ in tqdm(range(20), desc="Evaluation 1"):
		looser = arena.play_game(epsilon=0.1)
		if looser == 'red':
			p2_won += 1
		else:
			p1_won += 1

	arena.player1, arena.player2 = arena.player2, arena.player1

	for _ in tqdm(range(20), desc="Evaluation 2"):
		looser = arena.play_game(epsilon=0.1)
		if looser == 'red':
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