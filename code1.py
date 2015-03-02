## -*- coding: utf-8 -*-
import sys
import numpy
import random
import matplotlib.pyplot as plt
from pylab import *
from numpy.linalg import inv


covariancematrix=numpy.eye(4,4)
umean=1*numpy.ones(4).T
sigma0=1	

class priorWeight(object):
	"""docstring for priorWeight"""
	u=None
	cov=None
	step=None
	length=None
	covinv=None
	def __init__(self, step):
		super(priorWeight, self).__init__()
		self.step = step


class posteriorWeight(object):
	"""docstring for posteriorWeight"""
	u=None
	cov=None
	step=None
	length=None
	covinv=None
	def __init__(self, step):
		super(posteriorWeight, self).__init__()
		self.step = step

class Yt(object):
	"""docstring for Yt"""
	u=None 
	var=None 
	step=None 
	length=None 
	value=None
	def __init__(self, value,step):
		super(Yt, self).__init__()
		self.value=value
		self.step = step


class Xt(object):
	"""docstring for Xt"""
	value=None
	def __init__(self, value, step):
		super(Xt, self).__init__()
		self.step = step
		self.value=value

		

def initial(datamatrix,method):
	covariancematrix=numpy.eye(4,4)
	umean=0*numpy.ones(4).T
	priorweight=[]
	posteriorweight=[]
	yt=[]	
	xt=[]
	#create 10001 object, condition 0-10000	
	for i in range(0,10001):
		priorweight.append(priorWeight(i))
		#print priorweight[i].cov
		posteriorweight.append(posteriorWeight(i))
		if i==0:
			xt.append(Xt([1,1,1,1],i))
			yt.append(Yt(0,i))
		elif i!=0:
			xt.append(Xt(datamatrix[i-1,1:5],datamatrix[i-1,0]))
			yt.append(Yt(datamatrix[i-1,5],datamatrix[i-1,0]))
	priorweight=numpy.array(priorweight)
	posteriorweight=numpy.array(posteriorweight)
	yt=numpy.array(yt)
	xt=numpy.array(xt)
	return priorweight,posteriorweight,xt,yt
	

def readFile():
	data = open("stocks.txt","r")
	datalist = data.readlines()
	linecount=0
	#print len(datalist)
	infodata=[] #1000*5 matrix, the 1st column is the index of each data, the 2nd column is the data of A, 3rd B, 4th C, 5th D
	for line in datalist:
		linecount=linecount+1
		line=line.replace("\n","").split(",")
		if linecount>=3 and linecount<=10002:
			infodata.append([int(line[0])-1,float(line[1]),float(line[2]),float(line[3]),float(line[4]),float(line[5])])
	#print len(infodata)
	#print infodata[9999]
	datamatrix=numpy.array(infodata)
	return datamatrix

#w is 4*1, x^T is 1*4

# the model for question 1


def calculate(datamatrix,method):
	if method=="MO":
		size=10000
		sigma=1
		covsigma=numpy.eye(4,4)
		umean=0*numpy.ones(4).T
		priorweight,posteriorweight,xt,yt=initial(datamatrix,method)
		priorweight[0].u=umean
		priorweight[0].cov=covsigma
		priorweight[0].covinv=inv(priorweight[0].cov)
		posteriorweight[0].u=umean
		posteriorweight[0].cov=covsigma
		posteriorweight[0].covinv=inv(posteriorweight[0].cov)
		for t in range(1,size+1):
			priorweight[t].u=posteriorweight[t-1].u
			priorweight[t].cov=posteriorweight[t-1].cov
			priorweight[t].covinv=posteriorweight[t-1].covinv
			posteriorweight[t].cov=sigma**2*inv(sigma**2*priorweight[t].covinv+numpy.dot(xt[t].value.reshape(4,1),xt[t].value.reshape(1,4)))
			posteriorweight[t].covinv=priorweight[t].covinv+1/(sigma**2)*numpy.dot(xt[t].value.reshape(4,1),xt[t].value.reshape(1,4))
			tmp=numpy.dot(numpy.dot(posteriorweight[t].cov,priorweight[t].covinv),priorweight[t].u.reshape(4,1))
			posteriorweight[t].u=tmp+numpy.dot(yt[t].value/(sigma**2)*priorweight[t].cov,xt[t].value.reshape(4,1))
			if t==size:
				print posteriorweight[t].u,posteriorweight[t].cov,yt[t].value
	if method=="AB":
		size=10000
		sigma=1
		sigma0=0.25
		covsigma=numpy.array([[1,0.25,0,0],[0.25,1,0,0],[0,0,1,0],[0,0,0,1]])
		umean=0*numpy.ones(4).T
		priorweight,posteriorweight,xt,yt=initial(datamatrix,method)
		priorweight[0].u=umean
		priorweight[0].cov=covsigma
		priorweight[0].covinv=inv(priorweight[0].cov)
		posteriorweight[0].u=umean
		posteriorweight[0].cov=covsigma
		posteriorweight[0].covinv=inv(posteriorweight[0].cov)
		for t in range(1,size+1):
			priorweight[t].u=posteriorweight[t-1].u
			priorweight[t].cov=posteriorweight[t-1].cov
			priorweight[t].covinv=posteriorweight[t-1].covinv
			posteriorweight[t].cov=sigma**2*inv(sigma**2*priorweight[t].covinv+numpy.dot(xt[t].value.reshape(4,1),xt[t].value.reshape(1,4)))
			posteriorweight[t].covinv=priorweight[t].covinv+1/(sigma**2)*numpy.dot(xt[t].value.reshape(4,1),xt[t].value.reshape(1,4))
			tmp=numpy.dot(numpy.dot(posteriorweight[t].cov,priorweight[t].covinv),priorweight[t].u.reshape(4,1))
			posteriorweight[t].u=tmp+numpy.dot(yt[t].value/(sigma**2)*priorweight[t].cov,xt[t].value.reshape(4,1))
			if t==size:
				print posteriorweight[t].u,posteriorweight[t].cov,yt[t].value
	if method=="CD":
		size=10000
		sigma=1
		sigma0=0.25
		covsigma=numpy.array([[1,0,0,0],[0,1,0,0],[0,0,1,0.25],[0,0,0.25,1]])
		umean=0*numpy.ones(4).T
		priorweight,posteriorweight,xt,yt=initial(datamatrix,method)
		priorweight[0].u=umean
		priorweight[0].cov=covsigma
		priorweight[0].covinv=inv(priorweight[0].cov)
		posteriorweight[0].u=umean
		posteriorweight[0].cov=covsigma
		posteriorweight[0].covinv=inv(posteriorweight[0].cov)
		for t in range(1,size+1):
			priorweight[t].u=posteriorweight[t-1].u
			priorweight[t].cov=posteriorweight[t-1].cov
			priorweight[t].covinv=posteriorweight[t-1].covinv
			posteriorweight[t].cov=sigma**2*inv(sigma**2*priorweight[t].covinv+numpy.dot(xt[t].value.reshape(4,1),xt[t].value.reshape(1,4)))
			posteriorweight[t].covinv=priorweight[t].covinv+1/(sigma**2)*numpy.dot(xt[t].value.reshape(4,1),xt[t].value.reshape(1,4))
			tmp=numpy.dot(numpy.dot(posteriorweight[t].cov,priorweight[t].covinv),priorweight[t].u.reshape(4,1))
			posteriorweight[t].u=tmp+numpy.dot(yt[t].value/(sigma**2)*priorweight[t].cov,xt[t].value.reshape(4,1))
			if t==size:
				print posteriorweight[t].u,posteriorweight[t].cov,yt[t].value



def main(argv):
	datamatrix=readFile()
	#print datamatrix[100,1]
	calculate(datamatrix,"CD")
	#print yt[100].u
	#priorweight,posteriorweight,xt,yt=initial(datamatrix)
	#figure(1)
	#plt.plot(datamatrix[:,0],datamatrix[:,1:5])
	#plt.plot(datamatrix[:,0],datamatrix[:,1:4],'.')
	figure(2)
	plt.plot(datamatrix[:,0],datamatrix[:,5])
	#plt.plot(datamatrix[:,0],yt[:].u)
	#plt.show()
	#print x

if __name__ == "__main__":
     main(sys.argv)