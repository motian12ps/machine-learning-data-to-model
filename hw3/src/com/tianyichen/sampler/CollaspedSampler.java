package com.tianyichen.sampler;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Random;

import com.tianyichen.util.Document;
import com.tianyichen.util.Parameter;

public class CollaspedSampler {
	
	public static List<Document> TrainingDocuments=new ArrayList<Document>();
	public static List<Document> TestDocuments=new ArrayList<Document>();
	
	private static String trainingfile;
	private static String testfile;
	private static String outputDirectory;
	
	public static void main(String[] args){
		
		readParameters(args);
		
		TrainingDocuments=loadData(trainingfile);
		TestDocuments=loadData(testfile);
		
		Parameter.initializeParameter(TrainingDocuments, TestDocuments, args);
		
		
		trainingSamples();
		
		testSamples();
				
		outputResults();
		
		System.out.println("average runtime of each iteration of training documents="+Parameter.runtimeEachIteration);
		System.out.println("average runtime of each iteration of test documents="+Parameter.test_runtimeEachIteration);

		
		
	}
	
	private static void trainingSamples(){
		
		for(int iteration=0;iteration<Parameter.iterations;iteration++){
			
			//start time of current iteration
			long startTime=System.currentTimeMillis();
			
			for(int d=0;d<Parameter.N_d;d++){
				
				Document document=(Document) TrainingDocuments.get(d);
				
				for(int index_word=0;index_word<document.n_d_star;index_word++){
					int k=Parameter.z[d][index_word];
					int w=Document.vocabulary.get(document.wordList.get(index_word));
					
					Parameter.n_d_k[d][k]--;
					Parameter.n_k[k]--;
					Parameter.n_k_w[k][w]--;
					
					if(Parameter.x[d][index_word]==1){
						Parameter.n_c_k_w[document.corpus][k][w]--;
						Parameter.n_c_k[document.corpus][k]--;
					}
					
					
					Parameter.z[d][index_word]=sampleZ(d,index_word,w,document);
					int new_k=Parameter.z[d][index_word];
					
					Parameter.x[d][index_word]=sampleX(d,w,document,new_k);
					
					Parameter.n_d_k[d][new_k]++;

					Parameter.n_k[new_k]++;
					Parameter.n_k_w[new_k][w]++;

					if(Parameter.x[d][index_word]==1){
						Parameter.n_c_k_w[document.corpus][new_k][w]++;
						Parameter.n_c_k[document.corpus][new_k]++;
					}

				}
			}
			//estimate theta
			estimateTheta(TrainingDocuments,iteration);
			
			//estimate phi
			estimatePhi(TrainingDocuments,iteration);
			
			//estimate phic
			estimatePhic(TrainingDocuments,iteration);
			
			//calculate the loglikelihood at current iteration
			Parameter.loglikelihood[iteration]=computeTrainingLogLikelihood(TrainingDocuments);
			
			//end time of current iteration
			long endTime=System.currentTimeMillis();
			
			//total runtime
			Parameter.runtime[iteration+1]=Parameter.runtime[iteration]+(endTime-startTime);
			
			//Incorporate the current iteration runtime into average iteration runtime
			Parameter.runtimeEachIteration+=(endTime-startTime)/(double)Parameter.iterations;
			
			//print loglikelihood and runtime out
			System.out.println("iteration="+iteration+" training d=ocument: loglikelihood="+Parameter.loglikelihood[iteration]+" total runtime="+Parameter.runtime[iteration+1]);
			
		}
	}
	
	private static double computeTrainingLogLikelihood(List TrainingDocuments) {
		double loglikelihood=0;
		for(int d=0;d<Parameter.N_d;d++){
			Document document=(Document)TrainingDocuments.get(d);
			for(int index_word=0;index_word<document.n_d_star;index_word++){
				double logSum=0;
				int w=Document.vocabulary.get(document.wordList.get(index_word));
				for(int k=0;k<Parameter.K;k++){
					logSum+=Parameter.theta[d][k]*((1-Parameter.Lambda)*Parameter.phi_k_w[k][w]+Parameter.Lambda*Parameter.phi_c_k_w[document.corpus][k][w]);
					
				}
				loglikelihood+=Math.log(logSum);			
			}
		}
		return loglikelihood;

	}

	private static int sampleZ(int d,int i,int w,Document document){
		
		Double[] potential=new Double[Parameter.K];
		double sum_potential=0;
		
		for(int k=0;k<Parameter.K;k++){
			if(Parameter.x[d][i]==0){
				double expression1=(double)Parameter.n_d_k[d][k]+(double)Parameter.Alpha;
				double expression2=(double)document.n_d_star+(double)Parameter.K*(double)Parameter.Alpha;
				double expression3=(double)Parameter.n_k_w[k][w]+(double)Parameter.Beta;
				double expression4=(double)Parameter.n_k[k]+(double)Parameter.V*(double)Parameter.Beta;
				potential[k]=expression1*expression3/(expression2*expression4);
				sum_potential+=potential[k];
			}else if(Parameter.x[d][i]==1){
				double expression1=(double)Parameter.n_d_k[d][k]+(double)Parameter.Alpha;
				double expression2=(double)document.n_d_star+(double)Parameter.K*(double)Parameter.Alpha;
				double expression3=(double)Parameter.n_c_k_w[document.corpus][k][w]+(double)Parameter.Beta;
				double expression4=(double)Parameter.n_c_k[document.corpus][k]+(double)Parameter.V*(double)Parameter.Beta;
				potential[k]=expression1*expression3/(expression2*expression4);	
				sum_potential+=potential[k];
			}
		}
		
		Double[] multiNomial=new Double[Parameter.K];
		for(int k=0;k<Parameter.K;k++){
			multiNomial[k]=potential[k]/sum_potential;
		}
		
		Random random=new Random();
		double prob=random.nextDouble();
		double sum_prob=0;
		int index=0;
		while(true){
			sum_prob+=multiNomial[index];
			if(sum_prob>prob){
				return index;
			}
			index++;
		}
		
	} 
	
	private static int sampleX(int d, int w, Document document,int k){
		Double[] potential=new Double[2];
		double sum_potential=0;
		potential[0]=(1-(double)Parameter.Lambda)*((double)Parameter.n_k_w[k][w]+(double)Parameter.Beta)/((double)Parameter.n_k[k]+(double)Parameter.V*(double)Parameter.Beta);
		potential[1]=(double)Parameter.Lambda*((double)Parameter.n_c_k_w[document.corpus][k][w]+(double)Parameter.Beta)/((double)Parameter.n_c_k[document.corpus][k]+(double)Parameter.V*(double)Parameter.Beta);

		sum_potential=potential[0]+potential[1];
		
		Double[] multiNomial=new Double[Parameter.K];
		multiNomial[0]=potential[0]/sum_potential;
		multiNomial[1]=potential[1]/sum_potential;
		
		Random random=new Random();
		double prob=random.nextDouble();
		double sum_prob=0;
		int index=0;
		while(true){
			sum_prob+=multiNomial[index];
			if(sum_prob>prob){
				return index;
			}
			index++;
		}

	}
	
	private static void estimateTheta(List TrainingDocumens,int iteration){
		for(int d=0;d<Parameter.N_d;d++){
			Document document=(Document)TrainingDocuments.get(d);
			for(int k=0;k<Parameter.K;k++){
				Parameter.theta[d][k]=((double)Parameter.n_d_k[d][k]+(double)Parameter.Alpha)/((double)document.n_d_star+(double)Parameter.K*(double)Parameter.Alpha);
				if(iteration>=Parameter.burnIn){
					Parameter.final_theta[d][k]+=(Parameter.theta[d][k])/((double)(Parameter.iterations-Parameter.burnIn));
				}				
			}			
		}
	}
	
	private static void estimatePhi(List TrainingDocumens,int iteration){
		for(int k=0;k<Parameter.K;k++){
			for(int w=0;w<Parameter.V;w++){
				Parameter.phi_k_w[k][w]=((double)Parameter.n_k_w[k][w]+(double)Parameter.Beta)/((double)Parameter.n_k[k]+(double)Parameter.V*(double)Parameter.Beta);
				if(iteration>=Parameter.burnIn){
					Parameter.final_phi_k_w[k][w]+=(Parameter.phi_k_w[k][w])/((double)(Parameter.iterations-Parameter.burnIn));
					//System.out.println(Parameter.final_phi_k_w[k][w]);
				}
			}
		}
	}
	
	private static void estimatePhic(List TrainingDocumens,int iteration){
		for(int k=0;k<Parameter.K;k++){
			for(int w=0;w<Parameter.V;w++){
				for(int c=0;c<2;c++){
					Parameter.phi_c_k_w[c][k][w]=((double)Parameter.n_c_k_w[c][k][w]+(double)Parameter.Beta)/((double)Parameter.n_c_k[c][k]+(double)Parameter.V*(double)Parameter.Beta);
					if(iteration>=Parameter.burnIn){
						Parameter.final_phi_c_k_w[c][k][w]+=(Parameter.phi_c_k_w[c][k][w])/((double)(Parameter.iterations-Parameter.burnIn));
					}
				}
			}
		}
	}
	
	private static void testSamples(){
		
		for(int iteration=0;iteration<Parameter.iterations;iteration++){
			
			long startTime=System.currentTimeMillis();
			
			for(int d=0;d<Parameter.test_N_d;d++){
				
				Document document=(Document) TestDocuments.get(d);
				
				for(int index_word=0;index_word<document.n_d_star;index_word++){
					int k=Parameter.test_z[d][index_word];
					int w=Document.vocabulary.get(document.wordList.get(index_word));


					Parameter.test_n_d_k[d][k]--;

					if(Parameter.test_x[d][index_word]==1){
						Parameter.test_n_c_k_w[document.corpus][k][w]--;
						Parameter.test_n_c_k[document.corpus][k]--;				
					}

					
					Parameter.test_z[d][index_word]=sampleTestZ(d,index_word,w,document);
					int new_k=Parameter.test_z[d][index_word];
					
					Parameter.test_x[d][index_word]=sampleTestX(d,w,document,new_k);
					
					Parameter.test_n_d_k[d][new_k]++;

					if(Parameter.test_x[d][index_word]==1){
						Parameter.test_n_c_k_w[document.corpus][new_k][w]++;
						Parameter.test_n_c_k[document.corpus][new_k]++;
					}

				}
			}
			estimateTestTheta(TestDocuments,iteration);
			estimateTestPhic(TrainingDocuments,iteration);
			Parameter.test_loglikelihood[iteration]=computeTestLogLikelihood(TestDocuments);

			long endTime=System.currentTimeMillis();
			Parameter.test_runtime[iteration+1]=Parameter.runtime[iteration]+(endTime-startTime);
			Parameter.test_runtimeEachIteration+=(endTime-startTime)/(double)Parameter.iterations;
			System.out.println("iteration="+iteration+" test document: loglikelihood="+Parameter.test_loglikelihood[iteration]+" total test runtime="+Parameter.test_runtime[iteration+1]);
			
		}	

	}
	
	private static int sampleTestZ(int d,int i,int w,Document document){
		
		Double[] potential=new Double[Parameter.K];
		double sum_potential=0;
		
		for(int k=0;k<Parameter.K;k++){
			if(Parameter.test_x[d][i]==0){
				double expression1=(double)Parameter.test_n_d_k[d][k]+(double)Parameter.Alpha;
				double expression2=(double)document.n_d_star+(double)Parameter.K*(double)Parameter.Alpha;
				potential[k]=expression1/expression2*Parameter.phi_k_w[k][w];
				sum_potential+=potential[k];
			}else if(Parameter.test_x[d][i]==1){
				double expression1=(double)Parameter.test_n_d_k[d][k]+(double)Parameter.Alpha;
				double expression2=(double)document.n_d_star+(double)Parameter.K*(double)Parameter.Alpha;
				double expression3=(double)Parameter.test_n_c_k_w[document.corpus][k][w]+(double)Parameter.Beta;
				double expression4=(double)Parameter.test_n_c_k[document.corpus][k]+(double)Parameter.V*(double)Parameter.Beta;
				potential[k]=expression1*expression3/(expression2*expression4);	
				sum_potential+=potential[k];
			}
		}
		
		Double[] multiNomial=new Double[Parameter.K];
		for(int k=0;k<Parameter.K;k++){
			multiNomial[k]=potential[k]/sum_potential;
		}
		
		Random random=new Random();
		double prob=random.nextDouble();
		double sum_prob=0;
		int index=0;
		while(true){
			sum_prob+=multiNomial[index];
			if(sum_prob>prob){
				return index;
			}
			index++;
		}
		
	} 

	private static int sampleTestX(int d, int w, Document document,int k){
		Double[] potential=new Double[2];
		double sum_potential=0;
		potential[0]=(1-(double)Parameter.Lambda)*Parameter.final_phi_k_w[k][w];
		potential[1]=(double)Parameter.Lambda*((double)Parameter.n_c_k_w[document.corpus][k][w]+(double)Parameter.Beta)/((double)Parameter.n_c_k[document.corpus][k]+(double)Parameter.V*(double)Parameter.Beta);

		sum_potential=potential[0]+potential[1];
		
		Double[] multiNomial=new Double[Parameter.K];
		multiNomial[0]=potential[0]/sum_potential;
		multiNomial[1]=potential[1]/sum_potential;
		
		Random random=new Random();
		double prob=random.nextDouble();
		double sum_prob=0;
		int index=0;
		while(true){
			sum_prob+=multiNomial[index];
			if(sum_prob>prob){
				return index;
			}
			index++;
		}

	}	

	private static void estimateTestTheta(List TestDocuments,int iteration){
		for(int d=0;d<Parameter.test_N_d;d++){
			Document document=(Document)TestDocuments.get(d);
			for(int k=0;k<Parameter.K;k++){
				Parameter.test_theta[d][k]=((double)Parameter.test_n_d_k[d][k]+(double)Parameter.Alpha)/((double)document.n_d_star+(double)Parameter.K*(double)Parameter.Alpha);				
			}			
		}
	}

	private static void estimateTestPhic(List TestDocuments,int iteration){
		for(int k=0;k<Parameter.K;k++){
			for(int w=0;w<Parameter.V;w++){
				for(int c=0;c<2;c++){
					Parameter.test_phi_c_k_w[c][k][w]=((double)Parameter.test_n_c_k_w[c][k][w]+(double)Parameter.Beta)/((double)Parameter.test_n_c_k[c][k]+(double)Parameter.V*(double)Parameter.Beta);
				}
			}
		}
	}
	
	private static double computeTestLogLikelihood(List TestDocuments) {
		double loglikelihood=0;
		for(int d=0;d<Parameter.test_N_d;d++){
			Document document=(Document)TestDocuments.get(d);
			for(int index_word=0;index_word<document.n_d_star;index_word++){
				double logSum=0;
				int w=Document.vocabulary.get(document.wordList.get(index_word));
				for(int k=0;k<Parameter.K;k++){
					logSum+=Parameter.test_theta[d][k]*((1-Parameter.Lambda)*Parameter.final_phi_k_w[k][w]+Parameter.Lambda*Parameter.test_phi_c_k_w[document.corpus][k][w]);
				}
				loglikelihood+=Math.log(logSum);			
			}
		}
		return loglikelihood;

	}

	private static void outputResults(){
		
		try {

			PrintStream ps0=new PrintStream(new FileOutputStream(outputDirectory+"/collapsed-output-"+Parameter.K+"-"+Parameter.Lambda+"-"+Parameter.Alpha+".txt-theta"));
			PrintStream ps1=new PrintStream(new FileOutputStream(outputDirectory+"/collapsed-output-"+Parameter.K+"-"+Parameter.Lambda+"-"+Parameter.Alpha+".txt-phi"));
			PrintStream ps2=new PrintStream(new FileOutputStream(outputDirectory+"/collapsed-output-"+Parameter.K+"-"+Parameter.Lambda+"-"+Parameter.Alpha+".txt-phi0"));
			PrintStream ps3=new PrintStream(new FileOutputStream(outputDirectory+"/collapsed-output-"+Parameter.K+"-"+Parameter.Lambda+"-"+Parameter.Alpha+".txt-phi1"));
			PrintStream ps4=new PrintStream(new FileOutputStream(outputDirectory+"/collapsed-output-"+Parameter.K+"-"+Parameter.Lambda+"-"+Parameter.Alpha+".txt-trainll"));
			PrintStream ps5=new PrintStream(new FileOutputStream(outputDirectory+"/collapsed-output-"+Parameter.K+"-"+Parameter.Lambda+"-"+Parameter.Alpha+".txt-testll"));
			PrintStream ps6=new PrintStream(new FileOutputStream(outputDirectory+"/collapsed-output-"+Parameter.K+"-"+Parameter.Lambda+"-"+Parameter.Alpha+".txt-runtime-training"));
			PrintStream ps7=new PrintStream(new FileOutputStream(outputDirectory+"/collapsed-output-"+Parameter.K+"-"+Parameter.Lambda+"-"+Parameter.Alpha+".txt-runtime-test"));
			
			//output Theta
			for(int d=0;d<Parameter.N_d;d++){
				ps0.print(d+" ");
				for(int k=0;k<Parameter.K;k++){
					ps0.printf("%.13e",Parameter.final_theta[d][k]);
					ps0.append(" ");
				}
				ps0.println();
			}
			ps0.close();
			
			//Output phi
			
			Iterator iterator0=Document.vocabulary.keySet().iterator();
			while(iterator0.hasNext()){
				Object wordName=iterator0.next();
				int wordIndex=(Integer)Document.vocabulary.get(wordName);
				ps1.print(wordName+" ");
				for(int k=0;k<Parameter.K;k++){
					ps1.printf("%.13e", Parameter.final_phi_k_w[k][wordIndex]);
					ps1.append(" ");
					
				}
				ps1.println();
			}
			ps1.close();
			
			//output phi0
			Iterator iterator1=Document.vocabulary.keySet().iterator();
			while(iterator1.hasNext()){
				Object wordName=iterator1.next();
				int wordIndex=(Integer)Document.vocabulary.get(wordName);
				ps2.print(wordName+" ");
				for(int k=0;k<Parameter.K;k++){
					ps2.printf("%.13e", Parameter.final_phi_c_k_w[0][k][wordIndex]);
					ps2.append(" ");
					
				}
				ps2.println();
			}
			ps2.close();
			
			//output phi1
			Iterator iterator2=Document.vocabulary.keySet().iterator();
			while(iterator2.hasNext()){
				Object wordName=iterator2.next();
				int wordIndex=(Integer)Document.vocabulary.get(wordName);
				ps3.print(wordName+" ");
				for(int k=0;k<Parameter.K;k++){
					ps3.printf("%.13e", Parameter.final_phi_c_k_w[1][k][wordIndex]);
					ps3.append(" ");
					
				}
				ps3.println();
			}
			ps3.close();
			
			//output training loglikelihood
			
			for(int iteration=0;iteration<Parameter.iterations;iteration++){
				ps4.printf("%.13e", Parameter.loglikelihood[iteration]);
				ps4.println();
			}
			ps4.close();


			//Output test loglikelihood
			for(int iteration=0;iteration<Parameter.iterations;iteration++){
				ps5.printf("%.13e", Parameter.test_loglikelihood[iteration]);
				ps5.println();
			}
			ps5.close();
			
			for(int time_step=0;time_step<Parameter.iterations+1;time_step++){
				ps6.print(Parameter.runtime[time_step]);
				ps6.println();
			}
			ps6.close();
			
			for(int time_step=0;time_step<Parameter.iterations+1;time_step++){
				ps7.print(Parameter.test_runtime[time_step]);
				ps7.println();
			}
			ps7.close();


			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	
	private static List<Document> loadData(String fileName){
		
		File file=new File(fileName);
		BufferedReader reader=null;
		
		List<Document> documentsList = new ArrayList<Document>();
		
		try {
			reader=new BufferedReader(new FileReader(file));
			String line=null;
			while((line=reader.readLine())!=null){
				documentsList.add(new Document(line));
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
				
		return documentsList;
		
		
	}
	
	private static void readParameters(String[] args)
	{
		if (args.length == 9){
			
			CollaspedSampler.trainingfile=args[0];
			CollaspedSampler.testfile=args[1];
			CollaspedSampler.outputDirectory=args[2];
			Parameter.K=Integer.parseInt(args[3]);
			Parameter.Lambda=Double.parseDouble(args[4]);
			Parameter.Alpha=Double.parseDouble(args[5]);
			Parameter.Beta=Double.parseDouble(args[6]);
			Parameter.iterations=Integer.parseInt(args[7]);
			Parameter.burnIn=Integer.parseInt(args[8]);
			
		}else{
			
			CollaspedSampler.trainingfile="input-train.txt";
			CollaspedSampler.testfile="input-test.txt";
			CollaspedSampler.outputDirectory="beta";
			Parameter.K=25;
			Parameter.Lambda=0.5;
			Parameter.Alpha=0.1;
			Parameter.Beta=10;
			Parameter.iterations=1100;
			Parameter.burnIn=1000;
			
		}

	}


}
