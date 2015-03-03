from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from pyspark import SparkContext
import cPickle
import sys
import numpy
from scipy.linalg import eigh
from scipy.sparse.linalg import eigsh
import pyspark.rdd

num_features=100
num_slaves=5
num_dimension=1024
n1_eachslave=num_dimension/num_slaves

def unpickle(file):
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict
 
def main(argv):
 	#conf = SparkConf().setAppName('pca').setMaster('spark://albhed:7077')
 	#sc = SparkContext(conf=conf)
 	sc=SparkContext("local","Boost")
 	#inputfile = getArguments(argv)
 	#Uncomment following line to enable argument
 	#dict = unpickle(inputfile)
 	dict = unpickle('/Users/chentianyi/Documents/bigdata/cifar-10-batches-py/data_batch_1')
 	dt = unpickle('/Users/chentianyi/Documents/bigdata/cifar-10-batches-py/batches.meta')
 	print dt
 	#Initialize matrix
 	size = len(dict['data'])
 	featureSize = len(dict['data'][0])/3
 	grayMatrix = numpy.zeros((size, featureSize))
 	normalRGB = numpy.zeros((size, featureSize,3))


 
 	#Compute intensity and normalize
 	items = list(dict.items())
 	dataItem = items[0]
 	labels = numpy.array(dict['labels'])
 	#print labels
 	dataMatrix = numpy.array(dataItem[1])
 	R = dataMatrix[:,:1024]
 	G = dataMatrix[:,1024:2048]
 	B = dataMatrix[:,2048:]
 	#Construct original picture
 	normalRGB = numpy.rollaxis(numpy.asarray([R,G,B]), 0,3)
 	#Construct intensity Array
 	grayMatrix = (R*0.2989+G*0.5870+B*0.1140)
 	#Normalize
 	#grayMatrix -= grayMatrix.mean(axis=1)[:, None]
 	graMatrix=grayMatrix.T
 	train(grayMatrix, featureSize, labels)

def covariance(data):
	cov=numpy.cov(data,rowvar=1)
	return cov

def eigenvalue(data):
	e,EV = eigsh(data,num_features,which='LM')
	return e



def eigenvector(data):
	e,EV=eigsh(data,num_features,which='LM')
	return EV

def normalized(data):
	meanVals=numpy.mean(data)
	std=numpy.std(data)
	normal=(data-meanVals)/std
	print normal
	return normal

def svd(data):
	TOL=1e-8
	data=numpy.asarray(data)
	n=data.shape
	#print n[1]
	maxiteration=60
	U=data
	V=numpy.eye(n[0])
	singvals=numpy.zeros(n[0])
	print V
	converge=TOL+1
	countiteration=1
	while converge > TOL and countiteration<=maxiteration:
		countiteration=countiteration+1
		converge=0
		alpha=0
		beta=0
		gamma=0
		t=0
		for j in range(1,n[1]):
			for i in range(0,j):
				for k in range(0,n[1]):	
					alpha = alpha+U[k,i]*U[k,i]
					beta=beta+U[k,j]*U[k,j]
					gamma=gamma+U[k,i]*U[k,j]	
					converge=max(converge,abs(gamma)/numpy.sqrt(alpha*beta))
					#{alpha gamma;gamma beta}
					zeta=(beta-alpha)/(2*gamma)
				if zeta>0:
					t = 1/(numpy.abs(zeta)+numpy.sqrt(1+zeta*zeta))
				if zeta<0:
					t= -1/(numpy.abs(zeta)+numpy.sqrt(1+zeta*zeta))
					c = 1/numpy.sqrt(1+t^2)
					s = c*t

					#update columns i and j of U
					t=U[:,i]
					U[:,i]=c*t-s*U[:,j]
					U[:,j]=s*t-c*U[:,j]

					#update matrix V of eight sigunlar vectors
					t=V[:i]
					V[:,i]=c*t-s*V[:,j]
					V[:,j]=s*t+c*V[:,j]

		for j in range(0,n[1]):
			singvals[j]=numpy.linalg.norm(U)
			U[:,j]=U[:,j]/singvals[j];
		return singvals,U
		#print singvals
		#print U

def svdevl(data):
	TOL=1e-8
	data=numpy.asarray(data)
	n=size(data)
	#print n[1]
	maxiteration=60
	U=data
	V=numpy.eye(1024)
	singvals=numpy.zeros(1024)
	converge=TOL+1
	countiteration=1
	while converge > TOL and countiteration<=maxiteration:
		countiteration=countiteration+1
		converge=0
		alpha=0
		beta=0
		gamma=0
		t=0
		for j in range(1,n[1]):
			for i in range(0,j):
				for k in range(0,n[1]):	
					alpha = alpha+U[k,i]*U[k,i]
					beta=beta+U[k,j]*U[k,j]
					gamma=gamma+U[k,i]*U[k,j]	
					converge=max(converge,abs(gamma)/numpy.sqrt(alpha*beta))
					#{alpha gamma;gamma beta}
					zeta=(beta-alpha)/(2*gamma)
				if zeta>0:
					t = 1/(numpy.abs(zeta)+numpy.sqrt(1+zeta*zeta))
				if zeta<0:
					t= -1/(numpy.abs(zeta)+numpy.sqrt(1+zeta*zeta))
					c = 1/numpy.sqrt(1+t^2)
					s = c*t

					#update columns i and j of U
					t=U[:,i]
					U[:,i]=c*t-s*U[:,j]
					U[:,j]=s*t-c*U[:,j]

					#update matrix V of eight sigunlar vectors
					t=V[:i]
					V[:,i]=c*t-s*V[:,j]
					V[:,j]=s*t+c*V[:,j]

		for j in range(0,n[1]):
			singvals[j]=numpy.linalg.norm(U)
			U[:,j]=U[:,j]/singvals[j];	
		return singvals		
		#print singvals
		#print U

def plot(data):	
 	plt.imshow(data, cmap = cm.Greys_r)
 	plt.show()
 
def getArguments(argv):
 	if len(sys.argv) != 2:
 		print 'Please pass training file'
 		sys.exit()
 	return str(sys.argv[1])

def train(matrix, featureSize, labels):
	matrix=matrix.T
	RDD1=sc.parallelize(matrix) #set up the graMatrix on the spark
	normalized_data=RDD1.map(normalized) #normalized the original matrix
	covData=normalized_data.map(covariance)
	print covData.shape

def train1(matrix, featureSize, labels):
 	cov_mat = numpy.cov(matrix.T)
 	print cov_mat.shape
 	eig_val_cov, eig_vec_cov = numpy.linalg.eig(cov_mat)# Make a list of (eigenvalue, eigenvector) tuples
 	eg, vec = svd(matrix)
 	ep = [(numpy.abs(eg[i]), vec[:,i]) for i in range(len(eg))]
 	ep.sort()
 	ep.reverse()

 	print ep
 	eig_pairs = [(numpy.abs(eig_val_cov[i]), eig_vec_cov[:,i]) for i in range(len(eig_val_cov))]
 
 	# Sort the (eigenvalue, eigenvector) tuples from high to low
 	eig_pairs.sort()
 	eig_pairs.reverse()

 	print eig_pairs
 	#recData = transformed.dot(matrix_w.T) + matrix.mean(axis=1)[:, None]
 	#plot(recData[0].reshape((32,32)))
 			
 #Main entry
if __name__ == "__main__":
     main(sys.argv)