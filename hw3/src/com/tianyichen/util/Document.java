package com.tianyichen.util;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Document {
	public static Map<String,Integer> vocabulary=new HashMap<String,Integer>();
	private static int wordcounter=0;
	
	public List<String> wordList=new ArrayList<String>();
	
	//n_d_star is the number of words in each document instance
	public int n_d_star;
	public int corpus;
	
	//rewrite 
	public Document(String line){
		String[] line_split=line.replace("\n","").split(" ");
		this.corpus=Integer.parseInt(line_split[0]);
		
		for(int i=1;i<line_split.length;i++){
			this.wordList.add(line_split[i]);
			String word=line_split[i];
			
			//put the word in the entire vocabulary
			if(!Document.vocabulary.containsKey(word)){
				Document.vocabulary.put(word, Document.wordcounter++);
			}
		}
		this.n_d_star=this.wordList.size();

		
	}
	
	
	

}
