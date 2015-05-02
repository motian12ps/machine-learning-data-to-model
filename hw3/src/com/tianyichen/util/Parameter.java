package com.tianyichen.util;

import java.util.List;
import java.util.Random;

import com.tianyichen.sampler.*;
import com.tianyichen.util.*;



public class Parameter {
	
	//V is the size of Document.vocabulary
	public static int V;
	
	public static int K;
	
	public static double Lambda;
	
	public static double Alpha;
	
	public static double Beta;
	
	public static int iterations;
	
	public static int burnIn;
	
	//N_d is the number of documents in training documents
	public static int N_d;
	
	//z is the topic of each word in each document,this is a dynamic cell in training documents
	public static int[][] z;
	
	//x is the binary value of each document, this is a dynamic cell in training documents
	public static int[][] x;
	
	
	
	//theta the ratio of each document under each topic in training documents in training documents
	public static double[][] theta;
	
	//final theta is the incorporated theta after burnIn in training documents
	public static double[][] final_theta;
	
	//phi_k_w is ratio of each words in each document under each topic in training documents in training documents
	public static double[][] phi_k_w;
	 
	//final_phi_k_w is the incorporated phi_k_w after burnIn in training documents
	public static double[][] final_phi_k_w;
	
	//phi_c_k_w is ratio of each words in each document under each topic in training documents
	//which are corpus dependent in training documents
	public static double[][][] phi_c_k_w;
	
	//final_phi_c_k_w is the incorporated phi_c_k_w after burnIn in training documents
	public static double[][][] final_phi_c_k_w;
	
	//n_d_k is the number of topic's occurrence in each documents in training documents
	public static int[][] n_d_k;
	
	//n_k_w is the number of words under different topics in training documents
	public static int[][] n_k_w;
	
	//n_k is the number of topic's occurrence in training documents
	public static int[] n_k;
	
	public static int[][][] n_c_k_w;
	
	public static int[][] n_c_k;
	
	//loglikelihood at each iteration
	public static double[] loglikelihood;
	
	//test_N_d is the number of documents in test documents
	public static int test_N_d;
	
	public static int[][] test_z;
	public static int[][] test_x;
	
	public static double[][] test_theta;
	
	public static double[][][] test_phi_c_k_w;
	
	public static int[][] test_n_d_k;
	
	public static int[][][] test_n_c_k_w;
	
	public static int[][] test_n_c_k;
	
	public static double[] test_loglikelihood;
	
	public static long[] runtime;
	public static long[] test_runtime;
	
	public static double runtimeEachIteration;
	public static double test_runtimeEachIteration;
	
	public static void initializeParameter(List TrainingDocuments,List TestDocuments,String[] args){
		
		Parameter.V=Document.vocabulary.size();
		
		Parameter.N_d=TrainingDocuments.size();
		Parameter.test_N_d=TestDocuments.size();
		
		Parameter.theta=new double[Parameter.N_d][Parameter.K];
		Parameter.final_theta=new double[Parameter.N_d][Parameter.K];		
		Parameter.test_theta=new double[Parameter.test_N_d][Parameter.K];
		
		
		for(int d=0;d<Parameter.N_d;d++){
			for(int k=0;k<Parameter.K;k++){
				Parameter.final_theta[d][k]=0;
			}			
		}
		
		
		Parameter.phi_k_w=new double[Parameter.K][Parameter.V];
		Parameter.final_phi_k_w=new double[Parameter.K][Parameter.V];
		
		for(int k=0;k<Parameter.K;k++){
			for(int w=0;w<Parameter.V;w++){
				Parameter.final_phi_k_w[k][w]=0;
			}
		}
		
		Parameter.phi_c_k_w=new double[2][Parameter.K][Parameter.V];
		Parameter.final_phi_c_k_w=new double[2][Parameter.K][Parameter.V];		
		Parameter.test_phi_c_k_w=new double[2][Parameter.K][Parameter.V];
		
		for(int k=0;k<Parameter.K;k++){
			for(int w=0;w<Parameter.V;w++){
				Parameter.final_phi_c_k_w[0][k][w]=0;
				Parameter.final_phi_c_k_w[1][k][w]=0;
			}
		}
		
		Parameter.n_d_k=new int[Parameter.N_d][Parameter.K];
		Parameter.test_n_d_k=new int[Parameter.test_N_d][Parameter.K];
		
		Parameter.n_k_w=new int[Parameter.K][Parameter.V];
		Parameter.n_k=new int[Parameter.K];
		
		Parameter.n_c_k_w=new int[2][Parameter.K][Parameter.V];
		Parameter.test_n_c_k_w=new int[2][Parameter.K][Parameter.V];
		
		Parameter.n_c_k=new int[2][Parameter.K];
		Parameter.test_n_c_k=new int[2][Parameter.K];
		
		Parameter.z=new int[Parameter.N_d][];
		Parameter.x=new int[Parameter.N_d][];
		
		Parameter.test_z=new int[Parameter.test_N_d][];
		Parameter.test_x=new int[Parameter.test_N_d][];
		
		Parameter.loglikelihood=new double[Parameter.iterations];
		Parameter.test_loglikelihood=new double[Parameter.iterations];
		Parameter.runtime=new long[Parameter.iterations+1];
		Parameter.test_runtime=new long[Parameter.iterations+1];
		
		Parameter.runtime[0]=0;
		Parameter.test_runtime[0]=0;
		
		Parameter.runtimeEachIteration=0;
		Parameter.test_runtimeEachIteration=0;
		
		for(int d=0;d<Parameter.N_d;d++){
			
			Document document=(Document) TrainingDocuments.get(d);
			Parameter.z[d]=new int[document.n_d_star];
			Parameter.x[d]=new int[document.n_d_star];
			
			Random random=new Random();
			
			for(int index_word=0;index_word<document.n_d_star;index_word++){
				Parameter.x[d][index_word]=random.nextInt(2);
				//System.out.println(Parameter.x[d][index_word]);
				int k=random.nextInt(Parameter.K);
				//System.out.println(k);
				int w=Document.vocabulary.get(document.wordList.get(index_word));
				
				Parameter.n_d_k[d][k]++;
				Parameter.n_k_w[k][w]++;
				Parameter.n_k[k]++;
				
				if(Parameter.x[d][index_word]==1){
					Parameter.n_c_k_w[document.corpus][k][w]++;
					Parameter.n_c_k[document.corpus][k]++;
				}
				
				Parameter.z[d][index_word]=k;
				
			}		
									
		}
		
		for(int d=0;d<Parameter.test_N_d;d++){
			Document document=(Document) TestDocuments.get(d);
			
			Parameter.test_z[d]=new int[document.n_d_star];
			Parameter.test_x[d]=new int[document.n_d_star];
			
			Random random=new Random();
			
			for(int index_word=0;index_word<document.n_d_star;index_word++){
				
				Parameter.test_x[d][index_word]=random.nextInt(2);
				
				int k=random.nextInt(Parameter.K);
				int w=Document.vocabulary.get(document.wordList.get(index_word));
				

				Parameter.test_n_d_k[d][k]++;
				if(Parameter.test_x[d][index_word]==1){
					Parameter.test_n_c_k_w[document.corpus][k][w]++;
					Parameter.test_n_c_k[document.corpus][k]++;
				}
				
				Parameter.test_z[d][index_word]=k;
				
			}		
			
			
		}
		
		
	}
	
		
	
}
