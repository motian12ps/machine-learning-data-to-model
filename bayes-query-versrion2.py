#!/usr/bin/env python
## -*- coding: utf-8 -*-

# function getprob(str) returns the joint probability of the string
# To calculate conditional prob "str1 | str2", getprob(str1 + ',' + str2) / getprob(str2) 

import os
import sys, getopt
import numpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

nstates = []
variables = []
states = []
prob = []
joint = []
isroot = []
listfather = []

def main(argv):
	# network_filename cpd_filename lefthand_side [righthand_side]
	# Read and Initialization

	network_filename = "network-extended.txt" if len(argv)<2 else argv[1]
	cpd_filename = "cpd-extended.txt" if len(argv)<2 else argv[2]
	if len(argv)<3:
		input_string = "MaryGetsFlu=No"
	else:
		if len(argv)<5:
			input_string = argv[3]
		else:
			input_string = argv[3]+' '+argv[4]

	with open(network_filename,'r') as f:
		n = int(f.readline())
		nstates.append(1)
		
		for i in range(n):
			states.append([])
			line = f.readline()
			line1, line2 = line.split(' ')

			variables.append(line1)
			isroot.append(True)
			
			line2 = line2.strip()

			if line2.find(',') != -1:
				values = line2.split(',')
				for value in values:
					states[i].append(value)
			else:
				states[i].append(line2)

			nstates.append(nstates[i] * (len(states[i]) + 1))
			listfather.append([])

		for i in range(nstates[n]):
			prob.append([])
			for j in range(nstates[n]):
				prob[i].append(-1)
		for i in range(nstates[n]):
			joint.append(-1)

		for line in f:
			if line==None:
				father, child = line.strip().split(' -> ')
				isroot[getindex(child)] = False
				listfather[getindex(child)].append(father)
	
	with open(cpd_filename,'r') as f:
		for line in f:
			str1, str2, str3 = line.split(' ')
			a = strindex(str1)
			b = strindex(str2)
			prob[a][b] = float(str3)
			# if ',' not in str2 and root in str2:
			# 	joint[a + b] = joint[b] * prob[a][b]
			# 	print str1, str2, joint[a+b]
	for i in range(n):
		if isroot[i]:
			root = variables[i]
			for value in states[i]:
				joint[offset(root, value)] = 1.0 / len(states[i])
				prob[offset(root, value)][0] = 1.0 / len(states[i])

	for i in range(n):
		if isroot[i]:
			root = variables[i]
			for value in states[i]:
				init_reached = [False for j in range(n)]
				init_reached[i] = True
				calcprob(root + '=' + value, init_reached)
	strs = input_string.split(' ')
	if len(strs) == 1:
		str1 = strs[0]
		str2 = ''
	else:
		str1 = strs[0]
		str2 = strs[1]
	ans = getprob(str1)/getprob(str2)
	print '%.13e' % (ans)
	
	#Calculate Joint Probability

def calcprob(input_string, reached):
	index = strindex(input_string)
	new_reached = reached
	for variable in variables:
		if not reached[getindex(variable)]:
			# variable not in input_string:

			sen = input_string.split(',')
			flag = True
			
			for father in listfather[getindex(variable)]:
				if not reached[getindex(father)]:
					flag = False
					break

			if not flag:
				continue

			pindex = 0
			for phrase in sen:
				v, s = phrase.split('=')

				if phrase == '' or v not in listfather[getindex(variable)]:
					continue
				pindex += offset(v, s)

			for state in states[getindex(variable)]:
				new_string = input_string + ',' + variable + '=' + state

				a = strindex(new_string)
				b = strindex(variable + '=' + state)
				if a != b + index:
					print 'Error in index'

				if joint[a] != -1:
					break

				joint[a] = joint[index] * prob[b][pindex]
				# print joint[a], new_string

				new_reached[getindex(variable)] = True
				calcprob(new_string, new_reached)
				new_reached[getindex(variable)] = False
	return

def getprob(input_string):
	sen = input_string.split(',')
	if input_string == '':
		return 1
	index = strindex(input_string)	
	if joint[index] != -1:
		return joint[index]
	else:
		joint[index] = 0
		for variable in variables:
			
			flag = False
			for phrase in sen:
				v, s = phrase.split('=')
				if v == variable:
					flag = True

			if not flag:
				# print variable
				for state in states[getindex(variable)]:
					new_string = input_string + ',' + variable + '=' + state
					joint[index] += getprob(new_string)
				# print input_string, joint[index]
				return joint[index]

	joint[index] = 0
	return 0
	
def strindex(str1):
	# if str1 == '':
	# 	return 0
	a=0
	sen = str1.split(',')

	for phrase in sen:
		if phrase == '':
			continue
		variable, state = phrase.split('=')
		a += offset(variable, state)
	return a

def getindex(str1):
	for i in range(len(variables)):
		if variables[i] == str1:
			return i
	return -1

def offset(str1, str2):
	for i in range(len(variables)):
		if variables[i] == str1:
			for j in range(len(states[i])):
				if states[i][j] == str2:
					return (j + 1) * nstates[i]

if __name__ == '__main__':
	main(sys.argv)