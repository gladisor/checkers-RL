import torch
import torch.nn as nn
from checkers import Checkers
from dqn import DQN

class baseAgent():
	def __init__(self,
			step_size, discount, p_random_a):
		self.step_size = step_size
		self.discount = discount
		self.p_random_a = p_random_a

		self.state = None
		self.action = None

	def choose_action_egreedy(self, possible_actions):
		raise NotImplementedError

	def agent_start(self, state):
		raise NotImplementedError

	def agent_step(self, reward, next_state):
		raise NotImplementedError

	def agent_end(self, reward):
		raise NotImplementedError

class DQNAgent(baseAgent):
	def __init__(self, step_size, discount, p_random_a, n_hidden):
		baseAgent.__init__(self, step_size, discount, p_random_a)
		self.q = DQN(
			d_in=96, 
			d_hidden=64, 
			num_hidden=n_hidden).float()
		self.loss = nn.MSELoss()
		self.opt = torch.optim.Adam(self.q.parameters())
		self.memory = []

		self.state_action = None

	def action_to_vect(self, action):
		"""
		Converts action tuple of the form: (start_coord, end_coord)
		Returns onehot vector representation of that action
		"""
		start = self.coord_to_vect(action[0])
		end = self.coord_to_vect(action[1])
		final = np.concatenate((start, end))
		return final

	def generate_inputs(self, state, possible_actions):
		X = []
		for action in possible_actions:
			action = self.action_to_vect(action)
			action = torch.tensor(action).float()
			X.append(torch.cat((state, action)).float())

		X = torch.stack(X)
		return X

	def choose_action_egreedy(self, state, possible_actions):
		X = self.generate_inputs(state, possible_actions)
		q_vals = self.q(X)
		max_q = torch.argmax(q_vals).item()
		return possible_actions[max_q]

	def q_update(self, state_action, reward, next_state_action):
		current_q = self.q(state_action)
		target_q = reward + self.discount*self.q(next_state_action)
		error = self.loss(current_q, target_q)
		error.backward()
		self.opt.step()
		self.opt.zero_grad()

	def terminal_update(self, state_action, reward):
		current_q = self.q(state_action)
		error = self.loss(current_q, reward)
		error.backward()
		self.opt.step()
		self.opt.zero_grad()

	def agent_start(self, state, possible_actions):
		state = torch.tensor(state).float()
		action = self.choose_action_egreedy(state, possible_actions)
		action_vect = self.action_to_vect(action)
		self.state_action = torch.cat((self.state, action_vect))
		return action

	def agent_step(self, reward, next_state, possible_actions):
		next_state = torch.tensor(next_state).float()
		action = self.choose_action_egreedy(next_state, possible_actions)
		action_vect = self.action_to_vect(self.action)
		next_state_action = torch.cat((next_state, action_vect))
		self.q_update(self.state_action, reward, next_state_action)
		self.state_action = next_state_action
		return action

	def agent_end(self, reward):
		self.q_update(self.state_action, reward)



if __name__ == "__main__":
	red = DQNAgent(
		step_size=0.01,
		discount=0.80,
		p_random_a=0.1,
		n_hidden=5)

	black = DQNAgent(
		step_size=0.01,
		discount=0.80,
		p_random_a=0.1,
		n_hidden=5)

	env = Checkers()
	state = env.reset()
	env.render()

	possible_actions = env.get_possible_actions(env.board, 'red')
	action = red.agent_start(state, red_possible_actions)
	state, reward, terminal, hasNextMove = env.step(env.board, 'red', red_action)

	possible_actions = env.get_possible_actions(env.board, 'black')
	action = black.agent_start(state, black_possible_actions)

	colors = ['black', 'red']
	agents = [black, red]
	count = 0
	terminal = False
	while not terminal:
		color = colors[count]
		hasNextMove = True
		## Starts as red's turn
		while hasNextMove:
			state, reward, terminal, hasNextMove = env.step(env.board, color, action)
			possible_actions = env.get_possible_actions(env.board, color)
			action = agents[color].agent_step(reward, state, possible_actions)
			if terminal:
				break

		count = (count + 1) % 2



