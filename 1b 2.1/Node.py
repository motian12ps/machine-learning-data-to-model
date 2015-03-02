#!/MachineLearning
#DataStructure Node.py

class Node:

	def __init__(self, Name, States):
		'''Initializes every Node'''
		self.Name = Name
		self.States = States
		self.Position = 0

	def DocStrings(self):
		print self.Name,
		print self.States,

	def setPosition(self):
		self.Position = self.Position + 1
