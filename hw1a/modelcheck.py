## -*- coding: utf-8 -*-
import sys
import numpy
import random
import matplotlib.pyplot as plt
from pylab import *
from numpy.linalg import inv
import csv
from matplotlib.legend_handler import HandlerLine2D


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
	predicty=None
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
	infodata=[]
	with open('stocks.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for (num, A, B, C, D, Y) in reader:
			if num != "ms":
				infodata.append([int(num)-1,float(A), float(B), float(C), float(D), float(Y)])
	datamatrix=numpy.array(infodata)
	return datamatrix

#w is 4*1, x^T is 1*4

# the model for question 1


def calculate(datamatrix,method):

	if method is "MO":
		predictvalue=[]
		sumMSE=0
		aveMSE=0
		size=10000
		sigma=2.0
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
			posteriorweight[t].u=tmp+numpy.dot(yt[t].value/(sigma**2)*posteriorweight[t].cov,xt[t].value.reshape(4,1))
			sumMSE=sumMSE+(yt[t].value-numpy.dot(xt[t].value.reshape(1,4),posteriorweight[t].u.reshape(4,1)))**2
			predictvalue.append(numpy.dot(xt[t].value.reshape(1,4),posteriorweight[t].u.reshape(4,1)))
			if t==size:
				print "M_0:"
            	print posteriorweight[t].u
            	print posteriorweight[t].cov
            	aveMSE=sumMSE/10000
            	print aveMSE
            	return numpy.array(predictvalue)


	if method=="AB":
		predictvalue=[]
		sumMSE=0
		aveMSE=0
		size=10000
		sigma=2.0
		sigma0=numpy.sqrt(0.5)
		covsigma=numpy.array([[1,sigma0**2,0,0],[sigma0**2,1,0,0],[0,0,1,0],[0,0,0,1]])
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
			posteriorweight[t].u=tmp+numpy.dot(yt[t].value/(sigma**2)*posteriorweight[t].cov,xt[t].value.reshape(4,1))
			sumMSE=sumMSE+(yt[t].value-numpy.dot(xt[t].value.reshape(1,4),posteriorweight[t].u.reshape(4,1)))**2
			predictvalue.append(numpy.dot(xt[t].value.reshape(1,4),posteriorweight[t].u.reshape(4,1)))			
        	if t==size:
        		print "M_AB:"
        		print posteriorweight[t].u
        		print posteriorweight[t].cov
        		aveMSE=sumMSE/10000
        		print "M_AB average MSE", aveMSE
        		return numpy.array(predictvalue)

	if method=="CD":
		predictvalue=[]
		sumMSE=0
		aveMSE=0
		size=10000
		sigma=2.0
		sigma0=numpy.sqrt(0.5)
		covsigma=numpy.array([[1,0,0,0],[0,1,0,0],[0,0,1,sigma0**2],[0,0,sigma0**2,1]])
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
			posteriorweight[t].u=tmp+numpy.dot(yt[t].value/(sigma**2)*posteriorweight[t].cov,xt[t].value.reshape(4,1))
			sumMSE=sumMSE+(yt[t].value-numpy.dot(xt[t].value.reshape(1,4),posteriorweight[t].u.reshape(4,1)))**2
			predictvalue.append(numpy.dot(xt[t].value.reshape(1,4),posteriorweight[t].u.reshape(4,1)))
		aveMSE=sumMSE/10000
        if t==size:
            print "M_AB:"
            print posteriorweight[t].u
            print posteriorweight[t].cov
            aveMSE=sumMSE/10000
            print "M_CD average MSE", aveMSE
            return numpy.array(predictvalue)



def main(argv):
	datamatrix=readFile()
	predictyMO=calculate(datamatrix,"MO")
	predictyAB=calculate(datamatrix,"AB")
	predictyCD=calculate(datamatrix,"CD")
	figure(1)
	line1, =plt.plot(datamatrix[:,0],datamatrix[:,5],'.',color='blue',alpha=0.5,label='real y')
	line2, =plt.plot(datamatrix[:,0],predictyMO[:,0,0],'--',color='green',alpha=0.5,label='pred y_M_0')
	line3, =plt.plot(datamatrix[:,0],predictyAB[:,0,0],'-',color='pink',alpha=0.5,label='pred y_M_AB')
	line4, =plt.plot(datamatrix[:,0],predictyCD[:,0,0],'-',color='black',alpha=0.5,label='pred y_M_CD')
	plt.xlabel("t-step")
	plt.ylabel("Y")
	plt.title("Real y with prediction y by M_O,M_AB, and M_CD")
	first_legend=plt.legend(handler_map={line1:HandlerLine2D(4)})
	plt.show()

if __name__ == "__main__":
     main(sys.argv)