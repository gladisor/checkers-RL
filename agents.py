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
		self.state_action_pair = None

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

	def generate_inputs(self, state, possible_actions):
		X = []
		for action in possible_actions:
			action = env.action_to_vect(action)
			action = torch.tensor(action).float()
			X.append(torch.cat((state, action)).float())

		X = torch.stack(X)
		return X

	def choose_action_egreedy(self, state, possible_actions):
		X = self.generate_inputs(state, possible_actions)
		q_vals = self.q(X)
		max_q = torch.argmax(q_vals).item()
		return possible_actions[max_q], X[max_q]

	def agent_start(self, state, possible_actions):
		self.state = state
		self.action, self.state_action_pair = self.choose_action_egreedy(state, possible_actions)
		return self.action

	def agent_step(self, reward, next_state, possible_actions):
		current_q = self.q(self.state_action_pair)
		target_q = reward + self.discount*torch.max(self.q())

if __name__ == "__main__":
	agent = DQNAgent(
		step_size=0.01,
		discount=0.50,
		p_random_a=0.1,
		n_hidden=5)

	env = Checkers()
	state = env.reset()
	state = torch.tensor(state).float()

	possible_actions = env.get_possible_actions('red')

	print(agent.choose_action_egreedy(possible_actions))
	