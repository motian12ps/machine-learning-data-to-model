#!/MachineLearning
#DataStructure Main.py

import sys
from Node import Node

def Calculation_21(args_1, args_2, Nodes):

	#print args_1
	#print args_2
	args_11 = args_1[0].split("=")
	args_12 = args_1[1].split("=")
	args_21 = args_2[0].split("=")
	#print args_11
	#print args_12
	#print args_21

	#Condition 1:  M,R|F
	if args_11[0] == 'MaryGetsFlu' and args_12[0] == 'RoommateHasFlu':
		if args_12[1] == 'No' and args_21[1] == 'NotElevated':
			if args_11[1] == 'No':
				return float(Nodes[2].Probability_1[0][0])*float(Nodes[1].Probability_2[0][0])
			else:
				return float(Nodes[2].Probability_1[1][0])*float(Nodes[1].Probability_2[0][1])

		if args_12[1] == 'No' and args_21[1] == 'Elevated':
			if args_11[1] == 'No':
				return float(Nodes[2].Probability_1[0][2])*float(Nodes[1].Probability_2[0][0])
			else:
				return float(Nodes[2].Probability_1[1][2])*float(Nodes[1].Probability_2[0][0])

		if args_12[1] == 'Yes' and args_21[1] == 'NotElevated':
			if args_11[1] == 'No':
				return float(Nodes[2].Probability_1[0][1])*float(Nodes[1].Probability_2[1][0])
			else:
				return float(Nodes[2].Probability_1[1][1])*float(Nodes[1].Probability_2[1][0])

		if args_12[1] == 'Yes' and args_21[1] == 'Elevated':
			if args_11[1] == 'No':
				return float(Nodes[2].Probability_1[0][3])*float(Nodes[1].Probability_2[1][0])
			else:
				return float(Nodes[2].Probability_1[1][3])*float(Nodes[1].Probability_2[1][1])

	if args_11[0] == 'RoommateHasFlu' and args_12[0] == 'MaryGetsFlu':
		args = args_1[0]
		args_1[0] = args_1[1]
		args_1[1] = args
		return Calculation_21(args_1, args_2, Nodes)

	#Condition 2:  M,F|R
	if args_11[0] == 'MaryGetsFlu' and args_12[0] == 'FluRate':
		if args_12[1] == 'NotElevated' and args_21[1] == 'No':
			if args_11[1] == 'No':
				return float(Nodes[2].Probability_1[0][0])*float(Nodes[1].Probability_2[0][0])/(float(Nodes[1].Probability_2[0][0])+float(Nodes[1].Probability_2[0][1]))
			else:
				return float(Nodes[2].Probability_1[1][0])*float(Nodes[1].Probability_2[0][0])/(float(Nodes[1].Probability_2[0][0])+float(Nodes[1].Probability_2[0][1]))
		
		if args_12[1] == 'NotElevated' and args_21[1] == 'Yes':
			if args_11[1] == 'No':
				return float(Nodes[2].Probability_1[0][0])*float(Nodes[1].Probability_2[1][0])/(float(Nodes[1].Probability_2[1][0])+float(Nodes[1].Probability_2[1][1]))
			else:
				return float(Nodes[2].Probability_1[1][1])*float(Nodes[1].Probability_2[1][0])/(float(Nodes[1].Probability_2[1][0])+float(Nodes[1].Probability_2[1][1]))
		
		if args_12[1] == 'Elevated' and args_21[1] == 'No':
			if args_11[1] == 'No':
				return float(Nodes[2].Probability_1[0][2])*float(Nodes[1].Probability_2[0][1])/(float(Nodes[1].Probability_2[0][0])+float(Nodes[1].Probability_2[0][1]))
			else:
				return float(Nodes[2].Probability_1[1][2])*float(Nodes[1].Probability_2[0][1])/(float(Nodes[1].Probability_2[0][0])+float(Nodes[1].Probability_2[0][1]))

		if args_12[1] == 'Elevated' and args_21[1] == 'Yes':
			if args_11[1] == 'No':
				return float(Nodes[2].Probability_1[0][3])*float(Nodes[1].Probability_2[0][1])/(float(Nodes[1].Probability_2[1][0])+float(Nodes[1].Probability_2[1][1]))
			else:
				return float(Nodes[2].Probability_1[1][3])*float(Nodes[1].Probability_2[0][1])/(float(Nodes[1].Probability_2[1][0])+float(Nodes[1].Probability_2[1][1]))

	if args_11[0] == 'FluRate' and args_12[0] == 'MaryGetsFlu':
		args = args_1[0]
		args_1[0] = args_1[1]
		args_1[1] = args
		return Calculation_21(args_1, args_2, Nodes)

	#Condition 4: R,F|M
	if args_11[0] == 'RoommateHasFlu' and args_12[0] == 'FluRate':
		args = ''
		if args_1[0].split("=")[0] == 'MaryGetsFlu':
			args = args_1[0]
		if args_1[1].split("=")[0] == 'MaryGetsFlu':
			args = args_1[1]
		if args_2[0].split("=")[0] == 'MaryGetsFlu':
			args = args_2[0]
		return Calculation_1([args_1[0], args_1[1], args_2[0]], Nodes) / Calculation_10([args], Nodes)

	if args_11[0] == 'FluRate' and args_12[0] == 'RoommateHasFlu':
		args = args_1[0]
		args_1[0] = args_1[1]
		args_1[1] = args
		return Calculation_21(args_1, args_2, Nodes)

def Calculation_11(args_1, args_2, Nodes):

	args_11 = args_1[0].split("=")
	args_21 = args_2[0].split("=")

	#Condition 3:  M|F
	if args_11[0] == 'MaryGetsFlu' and args_21[0] == 'FluRate':
		return Calculation_21([args_1[0], 'RoommateHasFlu=No'], args_2, Nodes) + Calculation_21([args_1[0], 'RoommateHasFlu=Yes'], args_2, Nodes)

	#Condition 12:  R|M
	if args_11[0] == 'RoommateHasFlu' and args_21[0] == 'MaryGetsFlu':
		return Calculation_21([args_1[0], 'FluRate=NotElevated'], [args_2[0]], Nodes) + Calculation_21([args_1[0], 'FluRate=Elevated'], [args_2[0]], Nodes)

	#Condition 13:  F|M
	if args_11[0] == 'FluRate' and args_21[0] == 'MaryGetsFlu':
		return Calculation_21([args_1[0], 'RoommateHasFlu=No'], [args_2[0]], Nodes) + Calculation_21([args_1[0], 'RoommateHasFlu=Yes'], [args_2[0]], Nodes)

	#Condition 14:  M|R
	if args_11[0] == 'MaryGetsFlu' and args_21[0] == 'RoommateHasFlu':
		return Calculation_21([args_1[0], 'FluRate=NotElevated'], [args_2[0]], Nodes) + Calculation_21([args_1[0], 'FluRate=Elevated'], [args_2[0]], Nodes)

	#Condition 15:  F|R
	if args_11[0] == 'FluRate' and args_21[0] == 'RoommateHasFlu':
		return Calculation_21([args_1[0], 'MaryGetsFlu=No'], [args_2[0]], Nodes) + Calculation_21([args_1[0], 'MaryGetsFlu=Yes'], [args_2[0]], Nodes)

	#Condition 16:  R|F
	if args_11[0] == 'RoommateHasFlu' and args_21[0] == 'FluRate':
		return Calculation_21([args_1[0], 'MaryGetsFlu=No'], [args_2[0]], Nodes) + Calculation_21([args_1[0], 'MaryGetsFlu=Yes'], [args_2[0]], Nodes)

def Calculation_1(args_1, Nodes):
	#Condition 0:  M,P,F
	for i in range(0, 3):
		if args_1[i].split("=")[0] == "FluRate":
			args = args_1[i]
			args_1[i] = args_1[2]
			args_1[2] = args

	args_2 = [args_1[2]]
	args_1 = [args_1[0], args_1[1]]
	return Calculation_21(args_1, args_2, Nodes)*0.5

def Calculation_10(args_1, Nodes):
	
	args_11 = args_1[0].split("=")

	#Condition 4:  R
	if args_11[0] == 'RoommateHasFlu':
		if args_11[1] == 'No':
			return (float(Nodes[1].Probability_2[0][0]) + float(Nodes[1].Probability_2[0][1])) * 0.5
		if args_11[1] == 'Yes':
			return (float(Nodes[1].Probability_2[1][0]) + float(Nodes[1].Probability_2[1][1])) * 0.5

	#Condition 6:  M
	if args_11[0] == 'MaryGetsFlu':
		return Calculation_20([args_1[0], 'RoommateHasFlu=No'], Nodes) + Calculation_20([args_1[0], 'RoommateHasFlu=Yes'], Nodes)

	#Condition 17:  F
	if args_11[0] == 'FluRate':
		return 0.5

def Calculation_20(args_1, Nodes):

	args_11 = args_1[0].split("=")
	args_12 = args_1[1].split("=")

	#Condition 3:  M,R
	if args_11[0] == 'MaryGetsFlu' and args_12[0] == 'RoommateHasFlu':
		return (Calculation_21([args_1[0], 'FluRate=NotElevated'], [args_1[1]], Nodes) + Calculation_21([args_1[0], 'FluRate=Elevated'], [args_1[1]], Nodes)) * Calculation_10([args_1[1]], Nodes)

	if args_11[0] == 'RoommateHasFlu' and args_12[0] == 'MaryGetsFlu':
		args = args_1[0]
		args_1[0] = args_1[1]
		args_1[1] = args
		return Calculation_20(args_1, Nodes)

	#Condition 7:  M,F
	if args_11[0] == 'MaryGetsFlu' and args_12[0] == 'FluRate':
		return (Calculation_21([args_1[0], 'RoommateHasFlu=No'], [args_1[1]], Nodes) + Calculation_21([args_1[0], 'RoommateHasFlu=Yes'], [args_1[1]], Nodes)) * 0.5

	if args_11[0] == 'FluRate' and args_12[0] == 'MaryGetsFlu':
		args = args_1[0]
		args_1[0] = args_1[1]
		args_1[1] = args
		return Calculation_20(args_1, Nodes)

	#Condition 8:  R,M
	if args_11[0] == 'RoommateHasFlu' and args_12[0] == 'MaryGetsFlu':
		return Calculation_1([args_1[0], args_1[1], "FluRate=NotElevated"]) + Calculation_1([args_1[0], args_1[1], "FluRate=Elevated"])

	if args_11[0] == 'MaryGetsFlu' and args_12[0] == 'RoommateHasFlu':
		args = args_1[0]
		args_1[0] = args_1[1]
		args_1[1] = args
		return Calculation_20(args_1, Nodes)

def Calculation_12(args_1, args_2, Nodes):

	args_11 = args_1[0].split("=")
	args_21 = args_2[0].split("=")
	args_22 = args_2[1].split("=")

	#Condition 9:  M|F,R
	if args_21[0] == 'FluRate' and args_22[0] == 'RoommateHasFlu':
		if args_21[1] == 'NotElevated' and args_22[1] == 'No':
			if args_11[1] == 'No':
				return Nodes[2].Probability_1[0][0]
			else:
				return Nodes[2].Probability_1[1][0]
		if args_21[1] == 'NotElevated' and args_22[1] == 'Yes':
			if args_11[1] == 'No':
				return Nodes[2].Probability_1[0][1]
			else:
				return Nodes[2].Probability_1[1][1]
		if args_21[1] == 'Elevated' and args_22[1] == 'No':
			if args_11[1] == 'No':
				return Nodes[2].Probability_1[0][2]
			else:
				return Nodes[2].Probability_1[1][2]
		if args_21[1] == 'Elevated' and args_22[1] == 'Yes':
			if args_11[1] == 'No':
				return Nodes[2].Probability_1[0][3]
			else:
				return Nodes[2].Probability_1[1][3]

	if args_21[0] == 'RoommateHasFlu' and args_22[0] == 'FluRate':
		args = args_2[0]
		args_2[0] = args_2[1]
		args_2[1] = args
		return Calculation_12(args_1, args_2, Nodes)

	#Condition 10:  R|M,F
	if args_21[0] == 'MaryGetsFlu' and args_22[0] == 'FluRate':
		return Calculation_21([args_1[0], args_2[0]], [args_2[1]], Nodes) / Calculation_11([args_2[0]], [args_2[1]], Nodes)

	if args_21[0] == 'FluRate' and args_22[0] == 'MaryGetsFlu':
		args = args_2[0]
		args_2[0] = args_2[1]
		args_2[1] = args
		return Calculation_12(args_1, args_2, Nodes)

	#Condition 11:  F|M,R
	if args_21[0] == 'MaryGetsFlu' and args_22[0] == 'RoommateHasFlu':
		return Calculation_1([args_1[0], args_2[0], args_2[1]], Nodes) / Calculation_11([args_2[0]], [args_2[1]], Nodes) / Calculation_10([args_2[1]], Nodes)

	if args_21[0] == 'RoommateHasFlu' and args_22[0] == 'MaryGetsFlu':
		args = args_2[0]
		args_2[0] = args_2[1]
		args_2[1] = args
		return Calculation_12(args_1, args_2, Nodes)



args_1 = sys.argv[3]
print1 = args_1
if len(sys.argv) == 5:
	args_2 = sys.argv[4]
	print2 = args_2
else:
	args_2 = ''

myFile = file(sys.argv[1])
myProbability = file(sys.argv[2])

Nodes = [0, 1, 2]

everyLine = myFile.readline()

#Store all Nodes and States
for i in range(0, 3):
	everyLine = myFile.readline()
	LineStrings = everyLine.split(" ")
	LineStates = LineStrings[1].split(",")
	Nodes[i] = Node(LineStrings[0], LineStates)

#Store all relationships
for i in range(3, 6):
	everyLine = myFile.readline()
	LineStrings = everyLine.split(" -> ")

	for j in range(0, 3):

		if Nodes[j].Name + '\n' == LineStrings[1]:

			Nodes[j].setPosition()
			continue

for i in range(0, 3):
	if Nodes[i].Position == i:
		continue
	else:
		newNode = Nodes[i]
		Nodes[i] = Nodes[Nodes[i].Position]
		Nodes[newNode.Position] = newNode

#Store all probabilities
for i in range(0,12):
	everyLine = myProbability.readline()
	LineStrings = everyLine.split(" ")
	
	if LineStrings[0].split("=")[0] == 'MaryGetsFlu':

		Nodes[2].setProbability_1(LineStrings[0].split("=")[1], LineStrings[1].split(",")[0].split("=")[1], 
			LineStrings[1].split(",")[1].split("=")[1], LineStrings[2])
	
	if LineStrings[0].split("=")[0] == 'RoommateHasFlu':

		Nodes[1].setProbability_2(LineStrings[0].split("=")[1], LineStrings[1].split("=")[1], LineStrings[2])


#args_1 is lefthand
args_1 = args_1.split(",")

#args_2 is righthand
args_2 = args_2.split(",")

for i in range(0, len(args_1)):
	for j in range(0, len(args_2)):
		if args_1[i] == args_2[j]:
			del args_1[i]
			i -= 1
		if (args_1[i].split('=')[0] == args_2[j].split('=')[0]) and (args_1[i].split('=')[1] != args_2[j].split('=')[1]):
			print 0

if len(args_1) == 2 and len(args_2) == 1:
	if args_2[0] == '':
		result = Calculation_20(args_1, Nodes)
	elif len(args_1) == 2 and len(args_2) == 1:
		result = Calculation_21(args_1, args_2, Nodes)
elif len(args_1) == 1 and len(args_2) == 1:
	if args_2[0] == '':
		result = Calculation_10(args_1, Nodes)
	elif len(args_1) == 1 and len(args_2) == 1:
		result = Calculation_11(args_1, args_2, Nodes)
elif len(args_1) == 3 and len(args_2) == 1:
	if args_2[0] == '':
		result = Calculation_1(args_1, Nodes)
elif len(args_1) == 1 and len(args_2) == 2:
	result = Calculation_12(args_1, args_2, Nodes)


if len(sys.argv) == 5:
	print 'P(', print1, '|', print2, ') = ''%.13e'%(result)
else:
	print 'P(',print1,') = ''%.13e'%(result)

def judgeVertex(toJudge):
	
	if toJudge == MaryGetsFlu:
		return 2
	if toJudge == FluRate:
		return 0
	if toJudge == RoommateHasFlu:
		return 1

def judgeStatus(toJudge, allStates):
	if toJudge == allStates[0]:
		return 0
	if toJudge == allStates[1]:
		return 1
