#!/MachineLearning
#DataStructure Node.py

class Node:

	def __init__(self, Name, States):
		'''Initializes every Node'''
		self.Name = Name
		self.States = States
		self.Position = 0
		if Name == 'MaryGetsFlu':
			self.Probability_1 = [[0] * 4 for row in range(2)]
		if Name == 'RoommateHasFlu':
			self.Probability_2 = [[0] * 2 for row in range(2)]

	def DocStrings(self):
		print self.Name,
		print self.States,

	def setPosition(self):
		self.Position = self.Position + 1

	def setProbability_1(self, A_State, B_1_State, B_2_State, Probability):
		if A_State == 'No':
			if B_1_State == 'NotElevated':
				if B_2_State == 'No':
					i = 0
					j = 0
				if B_2_State == 'Yes':
					i = 0
					j = 1
			if B_1_State == 'Elevated':
				if B_2_State == 'No':
					i = 0
					j = 2
				if B_2_State == 'Yes':
					i = 0
					j = 3
		if A_State == 'Yes':
			if B_1_State == 'NotElevated':
				if B_2_State == 'No':
					i = 1
					j = 0
				if B_2_State == 'Yes':
					i = 1
					j = 1
			if B_1_State == 'Elevated':
				if B_2_State == 'No':
					i = 1
					j = 2
				if B_2_State == 'Yes':
					i = 1
					j = 3

		self.Probability_1[i][j] = Probability
		
	def setProbability_2(self, A_State, B_State, Probability):
		if A_State == 'No':
			if B_State == 'NotElevated':
				i = 0
				j = 0
			if B_State == 'Elevated':
				i = 0
				j = 1
		if A_State == 'Yes':
			if B_State == 'NotElevated':
				i = 1
				j = 0
			if B_State == 'Elevated':
				i = 1
				j = 1

		self.Probability_2[i][j] = Probability