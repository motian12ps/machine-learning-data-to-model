package com.tianyichen.recognition;

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
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import com.tianyichen.util.Inforvector;
import com.tianyichen.util.Parameter;


public class FenonicRecognition {
	
	//Mapping each feno to their corresponding fenomic Hmm
	public static Map<String,Hmm> fenoMap=new TreeMap<String, Hmm>();
	
	//Training pair <word, inforvector>
	//Since each word may have different fenem appearance, hence, value of map is a list of pair
	public static Map<String, List<Inforvector>> trainingPair=new TreeMap<String, List<Inforvector>>();
	
	//baseform of words
	public static Map<String, List<String>> baseForm=new TreeMap<String,List<String>>();

	public List<String> currentBaseform=new ArrayList<String>();
	
	//For dev labels, which are the testing labels.
	
	public static List<List<String>> devLabelList=new ArrayList<List<String>>();
	
	public static List<String> devWavList=new ArrayList<String>();
	
	//Alpha for trellis
	
	public static List<List<Double>> alpha=new ArrayList<List<Double>>();
	
	//beta for trellis
	
	public static List<List<Double>> beta=new ArrayList<List<Double>>();
	
	//coefficient 
	public static List<Double> coefficient=new ArrayList<Double>();	
	//sumStates
	public double sumStates;
	
	//loglikelihood
	
	public static List<Double> LogLikelihood=new ArrayList<Double>();	
	
	public static double numberSamples;
	
	public static void loadData(){
		
		numberSamples=0;
		
		trainingPair.clear();
		
		File trnscrFile=new File(Parameter.TrnScr);
		File trnwavFile=new File(Parameter.TrnWav);
		File trnlblsFile=new File(Parameter.TrnLbls);
		File trnendptsFile=new File(Parameter.Endpts);
		File devlblsFile=new File(Parameter.Devlbls);
		File devwavFile=new File(Parameter.DevWav);
		
		BufferedReader trnscrReader=null;
		BufferedReader trnwavReader=null;
		BufferedReader trnlblsReader=null;
		BufferedReader trnendptsReader=null;
		BufferedReader devlblsReader=null;
		BufferedReader devwavReader=null;
		
		
		try {
			trnscrReader=new BufferedReader(new FileReader(trnscrFile));
			trnwavReader=new BufferedReader(new FileReader(trnwavFile));
			trnlblsReader=new BufferedReader(new FileReader(trnlblsFile));
			trnendptsReader=new BufferedReader(new FileReader(trnendptsFile));
			devlblsReader=new BufferedReader(new FileReader(devlblsFile));
			devwavReader=new BufferedReader(new FileReader(devwavFile));
			
			//Since in each file, the first line is name of each file, we need to cut it
			trnscrReader.readLine();
			trnwavReader.readLine();
			trnlblsReader.readLine();
			trnendptsReader.readLine();
			devlblsReader.readLine();
			devwavReader.readLine();
			
			String line1=null;
			String line2=null;
			String line3=null;
			String line4=null;
			String line5=null;
			String line6=null;
			
			//Load training data
		
			while((line1=trnscrReader.readLine())!=null&&(line2=trnwavReader.readLine())!=null&&(line3=trnlblsReader.readLine())!=null){
				String word=line1;
				Inforvector inforvec=new Inforvector();
				List<String> fenem=new ArrayList<String>();
				
				inforvec.id=line2;
				//System.out.println(inforvec.id);
				//line3 is the data of fenems 
				String[] linesplit_3=line3.split(" ");
				
				for(int i=0;i<linesplit_3.length;i++){
					fenem.add(linesplit_3[i]);
					//System.out.println(linesplit_3[i]);
					numberSamples+=1;
				}
				
				inforvec.labelList=fenem;
				
				//line 4 is the start, end position information
				line4=trnendptsReader.readLine();
				String[] linesplit_4=line4.split(" ");

				inforvec.locationList[0]=Integer.parseInt(linesplit_4[0]);
				inforvec.locationList[1]=Integer.parseInt(linesplit_4[1]);
				//System.out.println(inforvec.locationList[0]+" "+inforvec.locationList[1]);
				
				int trainingcount=0;
				//if this is a new word
				if(trainingPair.get(word)==null){
					List<Inforvector> pairList=new ArrayList<Inforvector>();
					pairList.add(inforvec);
					trainingPair.put(word, pairList);
					//System.out.println(word+" "+trainingPair.get(word).get(0).id);
					
					//for the fenomic baseform for each word, it is <sil> AA, AB,AC....<sil>
					//where <sil> is the silence signal.
					List<String> base=new ArrayList<String>();
					base.add(Parameter.sil);
					for(int i=inforvec.locationList[0];i<inforvec.locationList[1]-1;i++){
						base.add(fenem.get(i));
					}
					base.add(Parameter.sil);
					baseForm.put(word, base);
					
//					for(int i=0;i<baseForm.get(word).size();i++){
//						System.out.print(baseForm.get(word).get(i)+" ");
//					}
//					System.out.println(baseForm.get(word).size());
					
				}else{ // word occurred in the past, add the inforvec into the existing vector
					List<Inforvector> pairList=trainingPair.get(word);
					pairList.add(inforvec);
					trainingPair.put(word, pairList);
					List<Inforvector> ll=trainingPair.get(word);

				}
				
							
			}
			
			//Load test(dev) data
			while((line5=devlblsReader.readLine())!=null && (line6=devwavReader.readLine())!=null){
				List<String> fenem=new ArrayList<String>();
				
				String[] linesplit_5=line5.split(" ");
				
				for(int i=0;i<linesplit_5.length;i++){
					fenem.add(linesplit_5[i]);
				}
				
				devLabelList.add(fenem);
				
				devWavList.add(line6);
				//System.out.println(line6);
								
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		


		
		
	}

	
	public FenonicRecognition(){
		Hmm.HMMIndexMap.clear();
		
		File LblNamesFile=new File(Parameter.LblNames);
		
		BufferedReader LblNamesReader=null;
		
		
		try {
			LblNamesReader=new BufferedReader(new FileReader(LblNamesFile));
			LblNamesReader.readLine();
			String line=null;
			int Hmmcount=0;
			while((line=LblNamesReader.readLine())!=null){
				fenoMap.put(line, new Hmm(line,Hmmcount));
				Hmm.HMMIndexMap.put(line, Hmmcount);
				Hmmcount++;

			}
			//System.out.println(Hmmcount);
			fenoMap.put(Parameter.sil, new Hmm(Parameter.sil,Parameter.fenonicSize-1));
			Hmm.HMMIndexMap.put(Parameter.sil, Parameter.fenonicSize-1);
			loadData();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
				
	}
	
	static int count=0;
	
	static int wordcount=0;
	
	public void Train(int iteration){
		
		LogLikelihood.clear();;
		
		double testsum=0.0;
		
		int insCount=0;
		
		Iterator it1=trainingPair.keySet().iterator();
		while(it1.hasNext()){
			wordcount++;
			
			
			
			insCount++;
			String word=(String) it1.next();
			
			testsum=testsum+trainingPair.get(word).size();
			//System.out.println(wordcount+" "+trainingPair.get(word).size()+" "+testsum);
			List<String> currentBaseForm=baseForm.get(word);

			List<Inforvector> instances=trainingPair.get(word);
			for(int j=0;j<instances.size();j++){
				
				List<String> observation=instances.get(j).labelList;
				
				List<Double> alpha0=new ArrayList<Double>();
				
				alpha.clear();
				beta.clear();
				coefficient.clear();
				
				
				sumStates=0.0;
				Iterator it2=currentBaseForm.iterator();
				
				while(it2.hasNext()){
					String fenom=(String) it2.next();

					for(int i=0;i<fenoMap.get(fenom).numofStates;i++){
						alpha0.add(1.0);
						sumStates++;
					}					
				}
				//Give uniform prior
				for(int i=0;i<alpha0.size();i++){
					alpha0.set(i, alpha0.get(i)/sumStates);

				}
				alpha.add(alpha0);
				

				
				collectCounts(observation,currentBaseForm);

			}
//			System.out.println();

		}
		
		
		//Estimate transition and emission probability
		Iterator it5=baseForm.keySet().iterator();
		while(it5.hasNext()){
			List<String> fenems=baseForm.get(it5.next());
			for(int i=0;i<fenems.size();i++){
				fenoMap.get(fenems.get(i)).UpdateProb(); //******UpdateProb
			}
		}
		
		//Reset counts
		Iterator it6=fenoMap.keySet().iterator();
		while(it6.hasNext()){
			fenoMap.get(it6.next()).Resetcounts(); //******Recounts
		}		
		double loglikelihood=0.0;
		for(int i=0;i<LogLikelihood.size();i++){
			loglikelihood+=LogLikelihood.get(i);
			
		}
		loglikelihood/=numberSamples;
		System.out.println("iteration:"+iteration+" loglikelihood:"+loglikelihood);

		
	}
	
	
	//static int count1=0;
	public void collectCounts(List<String> observation, List<String> currentBaseForm){
		
		double loglikelihood=0.0;

		
		
		//Initialize predict Alpha
		List<Double> predictAlpha=alpha.get(0);

		coefficient.add(1.0);
		
		
		
		//Alpha and Beta vector for each instance
		for(int i=0;i<observation.size();i++){
			
			List<Double> alphaList=new ArrayList<Double>();
			String obfe=observation.get(i);
			//for baseform trellis, compute alpha
		
			int feLoc=0;
			
			
			for(int j=0;j<currentBaseForm.size();j++){
				String feno=currentBaseForm.get(j);
				
				//HARD CODING
				//feno="AK";
				Hmm hmm=fenoMap.get(feno);
				
				alphaList=hmm.ForwardComputation(predictAlpha, feLoc, alphaList, obfe);
				//to be continued
				feLoc+=hmm.numofStates;
			}
			
			//Normalize alpha
			double sum=0.0;
			for(int j=0;j<alphaList.size();j++){
				sum+=alphaList.get(j);
			}
			for(int j=0;j<alphaList.size();j++){
				alphaList.set(j, alphaList.get(j)/sum);
				//System.out.println(alphaList.get(j));
			}
			
			loglikelihood+=Math.log(sum);
			
			coefficient.add(sum);
			predictAlpha=alphaList;
			
			
			try {
				FileWriter palpha = new FileWriter("alpha.out", true);
				BufferedWriter alpha_writer = new BufferedWriter(palpha);
				for (int j = 0; j < predictAlpha.size(); j++){
					alpha_writer.write(predictAlpha.get(j).toString() + " ");
				}
				alpha_writer.write("\n");
				alpha_writer.flush();
				palpha.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

			
			alpha.add(predictAlpha);
		}
		LogLikelihood.add(loglikelihood);
		//initialize beta
		List<Double> sucBeta=new ArrayList<Double>();
		List<Double> lastAlpha=alpha.get(alpha.size()-1);
		
		double coef=coefficient.get(coefficient.size()-1);
		//System.out.println(lastAlpha.size());
		for(int i=0;i<lastAlpha.size();i++){
			sucBeta.add(1.0/coef);
		}
		beta.add(0, sucBeta);
		
		//Update beta
		for(int i=observation.size()-1;i>=0;i--){
			List<Double> betaList=new ArrayList<Double>();
			//System.out.println(sumStates);
			int endLoc=(int) (sumStates-1);
			for(int j=currentBaseForm.size()-1;j>=0;j--){
				String feme=currentBaseForm.get(j);
				Hmm hmm=fenoMap.get(feme);
				betaList=hmm.BackwardComputation(alpha.get(i), coefficient.get(i), sucBeta, endLoc, betaList, observation.get(i));
				endLoc-=hmm.numofStates;
			}
			sucBeta=betaList;
			
			try {
				FileWriter betaba = new FileWriter("beta.out", true);
				BufferedWriter beta_writer = new BufferedWriter(betaba);
				for (int j = 0; j < predictAlpha.size(); j++){
					beta_writer.write(sucBeta.get(j).toString() + " ");
				}
				beta_writer.write("\n");
				beta_writer.flush();
				beta_writer.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			beta.add(0, sucBeta);
			
		}
		
	}
	
	static int testfilecount=0;
	//Given an sequence of fenems, find the most likely word
	public void predictMostlikelyword(){
		System.out.println("Predict word based on a sequence of fenomic bases");
		int count=0;
		for(int i=0;i<devLabelList.size();i++){
			findMostLikelyWord(devLabelList.get(i),devWavList.get(i));
		}
	}
	
	public void findMostLikelyWord(List<String> observation,String wavfile){
		List<String> currentbaseform=new ArrayList<String>();
		List<Double> sum=new ArrayList<Double>();
		
		testfilecount++;

		//System.out.println(testfilecount);
		String mostlikelyword=null;
		double maxloglikelihood=-10000.0;
		//double maxloglikelihood=Parameter.minusInfinity;
		Iterator it1=baseForm.keySet().iterator();
		while(it1.hasNext()){
			
			String currentword=(String) it1.next();
			
			currentbaseform=baseForm.get(currentword);

			double loglikelihood=0.0;
			
			List<Double> predictAlpha=new ArrayList<Double>();
			double sumStates=0.0;
			for(int i=0;i<currentbaseform.size();i++){
				String feme=currentbaseform.get(i);
				for(int j=0;j<fenoMap.get(feme).numofStates;j++){
					predictAlpha.add(1.0);
					sumStates+=1.0;
				}
			}

			for(int i=0;i<predictAlpha.size();i++){
				predictAlpha.set(i, predictAlpha.get(i)/sumStates);
				//System.out.print(predictAlpha.get(i)+" ");
			}
			
			for(int i=0;i<observation.size();i++){
				List<Double> alphaList=new ArrayList<Double>();
				String obfe=observation.get(i);
				//compute alpha from the initial fenem.
				int startLoc=0;
				
				
				for(int j=0;j<currentbaseform.size();j++){
					String feme=currentbaseform.get(j);
					Hmm hmm=fenoMap.get(feme);

					alphaList=hmm.ForwardComputation(predictAlpha, startLoc, alphaList, obfe);
					startLoc+=hmm.numofStates;
														
				}
				
				//Normalize alpha
				double sum1=0.0;
				for(int j=0;j<alphaList.size();j++){
					sum1+=alphaList.get(j);
				}
				for(int j=0;j<alphaList.size();j++){
					alphaList.set(j, alphaList.get(j)/sum1);
				}
				
				predictAlpha=alphaList;
				
//				for(int j=0;j<predictAlpha.size();j++){
//					System.out.print(predictAlpha.get(j)+" ");
//				}
//				System.out.println();
				
//				try {
//					FileWriter palpha = new FileWriter("testalpha.out", true);
//					BufferedWriter alpha_writer = new BufferedWriter(palpha);
//					for (int j = 0; j < predictAlpha.size(); j++){
//						alpha_writer.write(predictAlpha.get(j).toString() + " ");
//					}
//					alpha_writer.write("\n");
//					alpha_writer.flush();
//					palpha.close();
//				} catch (IOException e) {
//					// TODO Auto-generated catch block
//					e.printStackTrace();
//				}
				
				loglikelihood+=Math.log(sum1);
			}
			//System.out.println(currentword+" "+loglikelihood);
			if(loglikelihood>=maxloglikelihood){
				maxloglikelihood=loglikelihood;
				mostlikelyword=currentword;
			}
			//System.out.println(loglikelihood);
			sum.add(loglikelihood);
			
		}
		//System.out.println(maxloglikelihood);
		System.out.println("wav file: "+wavfile+", predict word: "+mostlikelyword);
		
		
	}
	
	public void printloglikelihood(int iteration){
	}
	
	public static void main(String[] args){
		
		System.out.println("Start training now:");
		FenonicRecognition fe1=new FenonicRecognition();
		
		long startTime=System.currentTimeMillis();
		
		for(int iteration=0;iteration<Parameter.iterations;iteration++){
			
			fe1.Train(iteration);
			
			fe1.printloglikelihood(iteration);		
			
		}
		long endTime=System.currentTimeMillis();
		long runtimeEachIteration=(long) ((endTime-startTime)/(double)Parameter.iterations);
		System.out.println("run time of each iteration="+runtimeEachIteration+"ms");
		
		fe1.predictMostlikelyword();

		
	}
	

	
}
