from game import Checkers
from dqn import DQN
from agent import Agent
from arena import Arena
from coach import Coach

from tqdm import tqdm
import torch
import torch.nn as nn

game = Checkers()
## Network to be trained using coach
dqn = DQN()

coach = Coach(
	game=game,
	nnet=dqn)

PATH = "models/testmodel.pt"

torch.save(coach.nnet.state_dict(), PATH)
coach.pnet.load_state_dict(torch.load(PATH))

loss = nn.MSELoss()
opt = torch.optim.Adam(coach.nnet.parameters(), lr=0.001)

examples = []
for _ in tqdm(range(10), desc="Self play"):
	X, target = coach.execute_episode(
		epsilon=0.3,
		gamma=0.80)



# opt.zero_grad()
# out = coach.nnet(X)
# error = loss(out, target)
# error.backward()
# opt.step()

torch.set_printoptions(sci_mode=False)
