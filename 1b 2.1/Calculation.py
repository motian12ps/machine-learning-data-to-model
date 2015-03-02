#!/MachineLearning
#DataStructure Node.py

from Node import Node

class Calculation:

	def Calculation(self, args_1, args_2, Nodes, Probs):
		
		self.args_1 = args_1.split(",")

		if len(self.args_1) == 2:

			for i in range(0, 3):

				if self.args_1[0].split("=")[0] == Nodes[i].Name:

					self.args_10 == Nodes[i].Position()
					break

			for j in range(0, 3):

				if self.args_1[1].split("=")[0] == Nodes[j].Name:

					self.args_11 == Nodes[j].Position()
					break

			if args_10 == 0 && args_11 == 1:
				
				if self.args_1[1].split("=")[1] == Nodes[i].States[0]:
					if self.args_2[1].split("=")[1] == Nodes[j].States[0]:
						if self.args_2[1].split("=")[1] == Nodes[j].States[0]







		if len(args_1.split() == 1):
			pass

