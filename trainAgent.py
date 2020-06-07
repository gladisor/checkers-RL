from dqn import DQN
from coach import Coach
from game import Checkers
from arena import Arena

import torch
from tqdm import tqdm

game = Checkers()
dqn = DQN()

NUM_EPOCHS = 80
NUM_TRAIN_GAMES = 200
NUM_EVAL_GAMES = 20
HALF = int(NUM_EVAL_GAMES/2)
TRAIN_EPSILON = 0.4
GAMMA = 0.8
EVAL_EPSILON = 0.01
LR = 0.0001
PATH = "models/test.pt"

coach = Coach(
	game=game,
	nnet=dqn,
	lr=LR)

num_improvements = 0
for _ in range(NUM_EPOCHS):
	## Saving a copy of the current network weights to pnet
	torch.save(coach.nnet.state_dict(), PATH)
	coach.pnet.load_state_dict(torch.load(PATH))

	for _ in tqdm(range(NUM_TRAIN_GAMES), desc="Self play"):
		data = coach.execute_episode(
			epsilon=TRAIN_EPSILON,
			gamma=GAMMA)

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
	for _ in tqdm(range(HALF), desc="Evaluation 1"):
		looser = arena.play_game(epsilon=EVAL_EPSILON)
		if looser == 'red':
			p2_won += 1
		else:
			p1_won += 1

	arena.player1, arena.player2 = arena.player2, arena.player1

	for _ in tqdm(range(HALF), desc="Evaluation 2"):
		looser = arena.play_game(epsilon=EVAL_EPSILON)
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
	print()