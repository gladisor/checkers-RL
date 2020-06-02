from dqn import DQN
from game import Checkers
import torch
import torch.nn as nn
from tqdm import tqdm

LOOSE_REWARD = -100
WIN_REWARD = 100

class Arena():
	def __init__(self, dqn, game):
		"""
		This class plays two agents against each other
		It records the results and all interactions in the games played
		"""
		self.dqn = dqn
		self.target_net = DQN().float()
		self.game = game

	def make_inputs(self, state, actions):
		state = torch.tensor(state)

		X = []
		for action in actions:
			action_vect = env.action_to_vect(action)
			action_vect = torch.tensor(action_vect)
			vect = torch.cat((state, action_vect))
			X.append(vect)
		X = torch.stack(X).float()
		return X

	def play_game(self, player1, player2, display=False):
		players = {
			'red': player1,
			'black': player2}

		prevStateAction = {
			'red': None,
			'black': None}

		trainingExamples = []
		self.game.reset()
		turn = 0
		## Red always starts
		curColor = 'red'
		board = self.game.board
		while not self.game.get_game_ended(board, curColor):
			self.game.get_game_ended(board, curColor)
			turn += 1
			## Get state and possible actions
			state = self.game.get_state(board, curColor)
			actions = self.game.get_possible_actions(board, curColor)
			## Action selection
			stateActions = self.make_inputs(state, actions)
			idx = players[curColor](stateActions)
			action = actions[idx]
			## Update training examples
			curStateAction = stateActions[idx]
			if prevStateAction[curColor] != None:
				## We store: prevStateAction, reward, all possible next stateActions
				# So that we can do a bellman optimality update:
				# q(S,A) <-- reward + gamma*max_a(q(S',a))
				trainingExamples.append([prevStateAction[curColor], 0, stateActions])
			prevStateAction[curColor] = curStateAction
			## If action was from black perspective we need to flip action
			# back to black perspective before we execute
			if curColor == 'black':
				action = self.game.flip_action(action)
			## Execute action
			prevColor = curColor
			board, curColor = self.game.get_next_state(board, curColor, action)
			## Print results
			if display:
				print(f"{prevColor}'s -> turn: {turn} action: {action}")
				print(board)
		trainingExamples.append([prevStateAction[curColor], LOOSE_REWARD, None])
		trainingExamples.append([prevStateAction[self.game.get_opponent_color(curColor)], WIN_REWARD, None])
		## Return looser color and training examples
		return curColor, trainingExamples

	def play_games(self, num, player1, player2):
		"""
		Lead agent plays num/2 games from red perspective
		then num/2 games from black perspective
		"""
		data = []
		leadAgentWins = 0
		lagAgentWins = 0
		halftime = int(num/2)
		for _ in tqdm(range(halftime), desc="Lead agent plays first"):
			result, trainingExamples = self.play_game(player1, player2)
			if result == 'red':
				lagAgentWins += 1
			elif result == 'black':
				leadAgentWins += 1
			data.extend(trainingExamples)

		## Switch players at halftime

		for _ in tqdm(range(halftime), desc="Lead agent plays second"):
			result, trainingExamples = self.play_game(player2, player1)
			if result == 'red':
				leadAgentWins += 1
			elif result == 'black':
				lagAgentWins += 1
			data.extend(trainingExamples)

		print(f"Win loss ratio: {leadAgentWins/(leadAgentWins+lagAgentWins)}")
		return leadAgentWins, lagAgentWins, data

	def learn(self, epochs, gamesPerEpoch, discount):
		"""
		Agent learns from data
		"""
		PATH = "models/dqn.pt"
		opt = torch.optim.Adam(self.dqn.parameters())
		loss = nn.MSELoss()

		torch.save(self.dqn.state_dict(), PATH)
		for epoch in range(epochs):
			self.target_net.load_state_dict(torch.load(PATH))

			player1 = lambda x: torch.argmax(self.dqn(x))
			player2 = lambda x: torch.argmax(self.target_net(x))

			leadAgentWins, lagAgentWins, data = self.play_games(gamesPerEpoch, player1, player2)

			SA = []
			R = []
			SA_ = []
			for row in data:
				SA.append(row[0])
				R.append(row[1])
				if row[2] != None:
					SA_.append(torch.max(self.target_net(row[2])).item())
				else:
					SA_.append(0)

			SA = torch.stack(SA)
			R = torch.tensor(R)
			SA_ = torch.tensor(SA_)

			opt.zero_grad()
			current_q = self.dqn(SA).squeeze()
			target_q = R + discount*SA_
			print(target_q.shape)
			error = loss(current_q, target_q)
			error.backward()
			opt.step()
			opt.zero_grad()
			torch.save(self.dqn.state_dict(), PATH)

if __name__ == "__main__":	
	dqn = DQN().float()
	env = Checkers()
	arena = Arena(dqn=dqn, game=env)

	arena.learn(
		epochs=10,
		gamesPerEpoch=10,
		discount=0.95)
			
