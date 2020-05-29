import torch
import torch.nn as nn
from checkers import Checkers

class baseAgent():
	def __init__(self,
			step_size, discount, p_random_a):
		self.step_size = step_size
		self.discount = discount
		self.p_random_a = p_random_a

		self.state = None
		self.action = None

class QAgent(baseAgent):
	def __init__(self):
		raise NotImplementedError

class DynaQAgent(QAgent):
	def __init__(self):
		raise NotImplementedError

class DQNAgent(baseAgent):
	def __init__(self):
		raise NotImplementedError

if __name__ == "__main__":
	