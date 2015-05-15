package com.tianyichen.util;

import java.util.HashMap;
import java.util.Map;

import com.tianyichen.recognition.Hmm;

public class Parameter {
	
	public static String LblNames="clsp.lblnames";
	public static String TrnScr="clsp.trnscr";
	public static String TrnWav="clsp.trnwav";
	public static String TrnLbls="clsp.trnlbls";
	public static String Endpts="clsp.endpts";
	public static String Devlbls="clsp.devlbls";
	public static String DevWav="clsp.devwav";
	public static int fenonicSize=257;
	public static Map<String, Integer> HIdxMap=new HashMap<String,Integer>();
	public static Map<String,Hmm> fenoMap = new HashMap<String,Hmm>();
	public static String sil="<sil>";
	public static double minusInfinity=-1000000000;
	public static int iterations=5;

}
