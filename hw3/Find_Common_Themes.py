#!/usr/bin/env python
import sys
import os
from operator import itemgetter

# if len(sys.argv) != 2:
# 	print 'usage: python topwords.py <phi_file>'
# 	exit()
phi = []
Z = []


# Change the input_file name here
input_file = []
input_file.append("output/collapsed-output-25-0.5-0.1.txt-phi")
input_file.append("output/collapsed-output-25-0.5-0.1.txt-phi0")
input_file.append("output/collapsed-output-25-0.5-0.1.txt-phi1")

#Read phi here
for (i, input_string) in enumerate(input_file):
	phi.append([])
	with open(input_string, 'r') as f:
		Z.append(len(f.readline().split()) - 1)  # number of topics

		for z in range(0, Z[i]): 
			phi[i].append({})

		f.seek(0)

		for line in f:
			tokens = line.split()
			word = tokens.pop(0)
			for z in range(0, Z[i]):
				phi[i][z][word] = float(tokens[z])

# Output the words and probabilities like topwords.py
# for i in range(3):
# 	for z in range(0, Z[i]):
# 		print 'Topic', z
# 		words = sorted(phi[i][z].items(), key=itemgetter(1), reverse=True)
# 		w = 0
# 		for word, p in words:
# 			print word#, p
# 			w += 1
# 			if w == 20: break
# 		print ''

# Keep the top 20 words for each topic
for i in range(3):
	for z in range(len(phi[i])):
		phi[i][z] = sorted(phi[i][z].items(), key=itemgetter(1), reverse=True)[:20]
		phi[i][z] = map(lambda arg: arg[0], phi[i][z])		

# Find the number of common top words
# Result saves the number of common top words for each topic
result = []
for z in range(Z[0]):
	result.append(0)
	for word in phi[0][z]:
		if word in phi[1][z] and word in phi[2][z]:
			result[z] = result[z] +1

print result
