#!/MachineLearning
#DataStructure Main.py

import Node
import Probability

args_1 = "MaryGetsFlu=Yes,FluRate=Elevated"
args_2 = "RoommateHasFlu=Yes"

myFile = file("network-simple.txt")
myProbability = file("cpd-simple.txt")

Nodes = [0, 1, 2]
Probs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

everyLine = myFile.readline()

#Store all Nodes and States
for i in range(0, 3):
	everyLine = myFile.readline()
	LineStrings = everyLine.split(" ")
	LineStates = LineStrings[1].split(",")
	Nodes[i] = Node.Node(LineStrings[0], LineStates)

m = 0

#Store all relationships
for i in range(3, 6):
	everyLine = myFile.readline()
	LineStrings = everyLine.split(" -> ")

	for j in range(0, 3):

		if Nodes[j].Name + '\n' == LineStrings[1]:

			Nodes[j].setPosition()
			continue

#Store all probabilities
for i in range(0,12):
	everyLine = myProbability.readline()
	LineStrings = everyLine.split(" ")
	
	if(len(LineStrings) == 2):
		Probs[i] = Probability2.Probability2(LineStrings[0].split('=')[0]
			, LineStrings[0].split("=")[1], LineStrings[1])

	if(len(LineStrings) == 3):
		Probs[i] = Probability.Probability(LineStrings[0].split("=")[0], 
			LineStrings[0].split("=")[1], LineStrings[1].split("=")[0], 
			LineStrings[1].split("=")[1], LineStrings[2])

#