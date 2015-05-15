package com.tianyichen.recognition;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import com.tianyichen.util.Parameter;


public class Hmm {
	
	//this map can map a name of hmm to its corresponding index
	public static Map<String, Integer> HMMIndexMap=new TreeMap<String, Integer>();
	public int numofStates;
	
	public String name;
	
	//transition matrix, where p is the normal transition matrix, q is the null transition matrix.
	public double pProb[][];
	public double qProb[][];
	public double pCount[][];
	public double qCount[][];
	
	//emission matrix
	public double eProb[][][];
	public double eCount[][][];
	
	
	
	
	public Hmm(String name, int index){
		this.name=name;
		
		//for silence HMM
		if(this.name==Parameter.sil){
			this.numofStates=7;
			
			//Initialize null transition 2*2 matrix
			this.pProb=new double[this.numofStates][this.numofStates];
			this.pCount=new double[this.numofStates][this.numofStates];
			for(int i=0;i<this.numofStates;i++){
				for(int j=0;j<this.numofStates;j++){
					this.pProb[i][j]=0.0;
					this.pCount[i][j]=0.0;
				}
			}
			
			//Initialize null transition 2*2 array
			this.qProb=new double[this.numofStates][this.numofStates];
			this.qCount=new double[this.numofStates][this.numofStates];
			for(int i=0;i<this.numofStates;i++){
				for(int j=0;j<this.numofStates;j++){
					this.qProb[i][j]=0.0;
					this.qCount[i][j]=0.0;
				}
			}
			
			//Initialize emission 3*3 matrix
			this.eProb=new double[this.numofStates][this.numofStates][Parameter.fenonicSize-1];
			this.eCount=new double[this.numofStates][this.numofStates][Parameter.fenonicSize-1];
			for(int i=0;i<this.numofStates;i++){
				for(int j=0;j<this.numofStates;j++){
					for(int k=0;k<Parameter.fenonicSize-1;k++){
						this.eProb[i][j][k]=1.0/256.0;
						this.eCount[i][j][k]=0;
					}
				}
			}
			
			//Set several prior normal transition prob
			this.pProb[0][1]=0.5;
			this.pProb[0][3]=0.5;
			this.pProb[1][1]=0.5;
			this.pProb[1][2]=0.5;
			this.pProb[2][2]=0.5;
			this.pProb[2][6]=0.5;
			this.pProb[3][4]=0.5;
			this.pProb[4][5]=0.5;
			this.pProb[5][6]=0.5;
			
			//set several prior null transition prob
			this.qProb[3][6]=0.5;
			this.qProb[4][6]=0.5;
			this.qProb[5][6]=0.5;
				
		}
		//For regular baseform,which is not silence signal
		else{
			//Assume the number of states is two.
			this.numofStates=2;
			
			//Initialize transition matrix 2*2
			this.pProb=new double[this.numofStates][this.numofStates];
			this.pCount=new double[this.numofStates][this.numofStates];
			
			for(int i=0;i<this.numofStates;i++){
				for(int j=0;j<this.numofStates;j++){
					this.pProb[i][j]=0;
					this.pCount[i][j]=0;
				}
			}
			
			//Initialize null transition 2*2 array
			this.qProb=new double[this.numofStates][this.numofStates];
			this.qCount=new double[this.numofStates][this.numofStates];
			for(int i=0;i<this.numofStates;i++){
				for(int j=0;j<this.numofStates;j++){
					this.qProb[i][j]=0.0;
					this.qCount[i][j]=0.0;
				}
			}
			
			//Initialize emission 3*3 matrix
			this.eProb=new double[this.numofStates][this.numofStates][Parameter.fenonicSize-1];
			this.eCount=new double[this.numofStates][this.numofStates][Parameter.fenonicSize-1];
			for(int i=0;i<this.numofStates;i++){
				for(int j=0;j<this.numofStates;j++){
					for(int k=0;k<Parameter.fenonicSize-1;k++){
						if(k==index){
							this.eProb[i][j][k]=0.5;
						}else{
							this.eProb[i][j][k]=0.5/255.0;
						}
						this.eCount[i][j][k]=0.0;
					}
				}
			}
			this.pProb[0][0]=0.1;
			this.pProb[0][1]=0.8;
			this.qProb[0][1]=0.1;
						
			
		}
	}
	
	//forward computation
	public List<Double> ForwardComputation(List<Double> predictAlpha, int startLoc, List<Double> alpha,String feme){
		
		//get index of HMM corresponding to the observed feme
		int index=Hmm.HMMIndexMap.get(feme);
		//System.out.println(feme);
		double last_a=0.0;
		if(!alpha.isEmpty()){
			last_a=alpha.get(alpha.size()-1);
			//System.out.println(al);
			//System.exit(0);
		}
		//First update non-null arc, j is source state, i is target state
		for(int i=0;i<this.numofStates;i++){

			for(int j=0;j<this.numofStates;j++){
				if(this.pProb[j][i]!=0){
					
					last_a+=predictAlpha.get(startLoc+j)*this.pProb[j][i]*this.eProb[j][i][index];
//					System.out.println("new pP al="+al);
				}
				if(this.qProb[j][i]!=0){
//					System.out.println(this.qProb[j][i]+" "+this.eProb[j][i][index]+" "+alpha.get(startLoc+j));

					last_a+=alpha.get(startLoc+j)*this.qProb[j][i];
//					System.out.println("new qP al="+al);
				}
//				System.out.println(al+" "+this.pProb[j][i]+" "+ this.qProb[j][i] +" "+this.eProb[j][i][index]);
			}

			alpha.add(last_a);
			last_a=0.0;
			
		}
		
		return alpha;
	}
	
	public List<Double> BackwardComputation(List<Double> alpha,double coef,List<Double> sucBeta, int endLoc, List<Double> beta,String feme){
		
		//get the index of corresponding HMM.
		int index=Hmm.HMMIndexMap.get(feme);
		
		double beta0=0.0;
		if(!beta.isEmpty()){
			beta0=beta.get(0);
		}
		beta.add(0, beta0);
		
		double sumb=0.0;
		
		for(int i=this.numofStates-2;i>=0;i--){
			for(int j=0;j<this.numofStates;j++){
				if(this.pProb[i][j]!=0){
					double bb=sucBeta.get(endLoc-(this.numofStates-j-1))*this.pProb[i][j]*this.eProb[i][j][index];
					double cc=alpha.get(endLoc-(this.numofStates-i-1))*bb;
					sumb+=bb/coef;
					
					this.eCount[i][j][index]+=cc;
					this.pCount[i][j]+=cc;
				}
				if(this.qProb[i][j]!=0){
					sumb+=this.qProb[i][j]*beta0;
					this.qCount[i][j]+=alpha.get(endLoc-(this.numofStates-i-1))*this.qProb[i][j]*beta0*coef;
					
				}
			}
			beta.add(0, sumb);
			sumb=0.0;
		}
		//System.out.println(sumb+" "+beta.size());
		return beta;
		
	}
	
	
	//Update Probability
	public void UpdateProb(){
		for(int i=0;i<this.numofStates;i++){
			double denom=0.0;
			for(int j=0;j<this.numofStates;j++){
				denom+=(this.pCount[i][j]+this.qCount[i][j]);
				
				if(this.pCount[i][j]!=0){
					double sumK=0.0;
					for(int k=0;k<Parameter.fenonicSize-1;k++){
						//System.out.println(i+" "+j+" "+k+" "+this.pCount[i][j]+" "+this.qCount[i][j]+" "+this.eCount[i][j][k]);
						sumK+=this.eCount[i][j][k];
					}
					for(int k=0;k<Parameter.fenonicSize-1;k++){
						this.eProb[i][j][k]=this.eCount[i][j][k]/sumK;
						//System.out.println(i+" "+j+" "+k+" "+this.pProb[i][j]+" "+this.qProb[i][j]+" "+this.eProb[i][j][k]);
					}
				}
			}
			//this.numofStat
			for(int j=0;j<this.numofStates;j++){
				if(denom!=0){
					this.pProb[i][j]=this.pCount[i][j]/denom;
					this.qProb[i][j]=this.qCount[i][j]/denom;
				}
			}
		}
	}
	
	public void Resetcounts(){
		
		for(int i=0;i<this.numofStates;i++){
			for(int j=0;j<this.numofStates;j++){
				this.pCount[i][j]=0;
				this.qCount[i][j]=0;
				for(int k=0;k<Parameter.fenonicSize-1;k++){
					this.eCount[i][j][k]=0;
				}
			}
		}
	}
	

	
}
