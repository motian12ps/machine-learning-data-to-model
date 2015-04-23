#!/usr/bin/env python
import sys
import math
import numpy as np
from collections import defaultdict

class HMM:

	def __init__(self, numOfStates=1, numOfSymbols=1, startProb=None, transProb=None, emissionProb=None, numOfIter=50, convThresh=1e-5, isArc=False):
		self.numOfStates = numOfStates
		self.numOfSymbols = numOfSymbols
		self.startProb = startProb
		self.transProb = transProb
		self.emissionProb = emissionProb
		self.numOfIter = numOfIter
		self.convThresh	= convThresh
		self.isArc = isArc
		self.logProb = []
		self.characterProb = defaultdict(list)

	def train(self, obs):
		"""Train HMM Model given observations

		obs: array, shape('length of observations sequence')

		"""


		it = 0
		self.diff = np.inf
		while it < 2:
		# while it < self.numOfIter and self.diff > self.convThresh:
			it += 1
			print it
			self.em(obs)


	def forward(self, obs):
		if self.startProb == None:
			print 'Start probability is not set'
			return
		self.alpha = np.zeros((self.numOfStates, len(obs)))
		#Coefficient that normalize each column of alpha
		self.coef = np.zeros(len(obs))

		#If arc transition
		if self.isArc:
			#TODO
			pass
		#state emission
		else:
			self.alpha[:,0] = self.startProb * self.emissionProb[:,obs[0]]
			self.coef[0] =  np.sum(self.alpha[:,0])
			self.alpha[:,0] /= self.coef[0]
			for n in range(1,len(obs)):
				self.alpha[:,n] = np.dot(self.alpha[:,n-1], self.transProb) * self.emissionProb[:,obs[n]]
				self.coef[n] = np.sum(self.alpha[:,n])
				self.alpha[:,n] /= self.coef[n]

		#Record log probability
		self.logProb.append(np.sum(np.log(self.coef))/len(obs))
		print self.alpha
		return self.alpha

	def backword(self, obs):

		self.beta = np.zeros((self.numOfStates, len(obs)))
		self.beta[:,len(obs)-1] = 1/self.coef[len(obs)-1]

		if self.isArc:
			#TODO
			pass
		#state emission
		else:
			for n in range(1,len(obs)):
				loc = len(obs) - n
				self.beta[:,loc-1] = np.dot(self.transProb, self.emissionProb[:,obs[loc]] * self.beta[:,loc])
				self.beta[:,loc-1] /= self.coef[loc-1]

		return self.beta

	def em(self, obs):

		self.forward(obs)
		self.backword(obs)

		#Collect sigma
		sigma = np.zeros((len(obs)-1, self.numOfStates, self.numOfStates))
		# alpha * beta
		gamma = self.alpha * self.beta

		for t in range(len(obs) - 1):
			#Denominator is all possible transitions between alpha[t] and beta[t+1], emitting obs[t]
			denom = 0.0
			#Compute transition through one state
			for i in range(self.numOfStates):
				for j in range(self.numOfStates):
					sigma[t,i,j] = self.alpha[i][t] * self.transProb[i][j] * self.beta[j][t+1] * self.emissionProb[j][obs[t+1]]
					denom += sigma[t,i,j]
			sigma[t] /= denom
		
		#Collect gamma
		gamma /= np.sum(gamma, axis = 0)

		#Re-estimate parameters
		#For transition probability
		self.oldTransProb = self.transProb
		for state in range(self.numOfStates):
			self.transProb[state,:] = np.sum(sigma,axis=0)[state,:] / np.sum(gamma[state,:])
			#Normalize
			self.transProb[state,:] /= np.sum(self.transProb[state,:])

		#Update date start probability
		self.oldStartProb = self.startProb
		self.startProb = gamma[:,0]

		#For emission probability
		self.oldEmissionProb = self.emissionProb
		self.emissionProb = np.zeros((self.numOfStates, self.numOfSymbols))
		stateDenom = np.sum(gamma, axis=1)
		for t in range(len(obs)):
			for state in range(self.numOfStates):
				self.emissionProb[state][obs[t]] += gamma[state][t] / stateDenom[state]

		self.diff = np.sum(np.sum(abs(self.transProb - self.oldTransProb))) + np.sum(np.sum(abs(self.emissionProb - self.oldEmissionProb))) \
			+ np.sum(abs(self.startProb - self.oldStartProb))

	def viterbi(self, obs):

		# Initialize path to be a list with length of observation sequence
		path = [[] for seq in range(self.numOfStates)]
		# Base case
		prob = self.startProb * self.emissionProb[:,obs[0]]
		#Start to find path
		for t in range(1, len(obs)):
			probArray = (prob * self.transProb.T).T * self.emissionProb[:,obs[t]]
			#Find maximum for each column, to be the best probability and the backpoint
			prob = probArray.max(axis=0)
			backPoint = probArray.argmax(axis=0)
			[path[state].append(backPoint[state]) for state in range(self.numOfStates)]

		#Get max for the last state, and append it to the path
		lastMaxState = prob.argmax()
		path[lastMaxState].append(lastMaxState)
		return path[lastMaxState]

#Test below
def main(argv):
	numOfStates = 2
	numOfSymbols = 2
	hmm = HMM(numOfStates, numOfSymbols)
	hmm.startProb = np.array([0.85, 0.15])
	hmm.transProb = np.array([[0.3, 0.7], [0.1, 0.9]])
	hmm.emissionProb = np.array([[0.4, 0.6], [0.5, 0.5]])

	obs = np.array([0,1,1,0])
	hmm.train(obs)
	print "transProb",hmm.transProb
	print "emissionProb",hmm.emissionProb
	print hmm.logProb
#Main entry
if __name__ == '__main__':
	main(sys.argv)
