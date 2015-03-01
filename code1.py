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
	def __init__(self, step):
		super(Yt, self).__init__()
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
	umean=0.75*numpy.ones(4).T
	priorweight=[]
	posteriorweight=[]
	yt=[]	
	xt=[]
	#create 10001 object, condition 0-10000	
	for i in range(0,10001):
		priorweight.append(priorWeight(i))
		#print priorweight[i].cov
		posteriorweight.append(posteriorWeight(i))
		yt.append(Yt(i))
		if i==0:
			xt.append(Xt([1,1,1,1],i))
		elif i!=0:
			xt.append(Xt(datamatrix[i-1,1:5],datamatrix[i-1,0]))
	priorweight=numpy.array(priorweight)
	posteriorweight=numpy.array(posteriorweight)
	yt=numpy.array(yt)
	xt=numpy.array(xt)
	if method=="MO":
		priorweight[0].u=umean
		priorweight[0].cov=covariancematrix
		priorweight[0].covinv=inv(priorweight[0].cov)
		posteriorweight[0].u=umean
		posteriorweight[0].cov=covariancematrix
		posteriorweight[0].covinv=inv(posteriorweight[0].cov)
		yt[0].u=0
		yt[0].var=sigma0
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
def calculate1(datamatrix,method):
	size=10000
	priorweight,posteriorweight,xt,yt=initial(datamatrix,method)
	for t in range(1,size+1):
		priorweight[t].u=posteriorweight[t-1].u
		priorweight[t].cov=posteriorweight[t-1].cov
		priorweight[t].covinv=posteriorweight[t-1].covinv
		#print priorweight[t].covinv
		yt[t].u=numpy.dot((xt[t].value.reshape(1,4)),priorweight[t].u.reshape(4,1))
		yt[t].var=sigma0**2+numpy.dot(numpy.dot(xt[t].value.reshape(1,4),priorweight[t].cov),xt[t].value.reshape(4,1))
		#print yt[t].var
		#print yt[t].u
		# ** 是算术
		#print numpy.dot(xt[t].value.reshape(4,1),xt[t].value.reshape(1,4)),xt[t].value.reshape(4,1)*xt[t].value.reshape(1,4)
		posteriorweight[t].cov=yt[t].var**2*inv((yt[t].var**2*priorweight[t].covinv+numpy.dot(xt[t].value.reshape(4,1),xt[t].value.reshape(1,4))))
		#posteriorweight[t].covinv=priorweight[t].covinv+1/(sigma0**2)*xt[t].value.reshape(4,1)*xt[t].value.reshape(1,4)
		posteriorweight[t].covinv=inv(posteriorweight[t].cov)
		#print numpy.dot(posteriorweight[t].cov,posteriorweight[t].covinv)
		tmp=numpy.dot(numpy.dot(posteriorweight[t].cov,priorweight[t].covinv),priorweight[t].u.reshape(4,1))
		#print tmp
		posteriorweight[t].u=tmp+1/(yt[t].var**2)*numpy.dot(posteriorweight[t].cov,xt[t].value.reshape(4,1)*yt[t].u)
		#print posteriorweight[t].u
		if t==size-1:
			print posteriorweight[t].u,posteriorweight[t].cov,yt[t].u
	#print posteriorweight[size-1].u,posteriorweight[size-1].cov
	#print yt[size-1].u
	return yt




def main(argv):
	datamatrix=readFile()
	#print datamatrix[100,1]
	yt=calculate1(datamatrix,"MO")
	print yt[100].u
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