
class TauBuffer(object):

	def __init__(self):
		self.buffer = []

	def add_rollout(self, tau):
		self.buffer.append(tau)

	def get_rollout(self, i):
		return self.buffer[i]

class Rollout(object):
	def __init__(self, step_tuples):
		self.step_tuples = step_tuples

	def at_step(self, i):
		observation, reward, done, info = self.step_tuples[i]
		return observation, reward, done, info