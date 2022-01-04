
import java.io.FileInputStream;

import java.io.IOException;
import java.io.InputStream;
import java.text.DecimalFormat;
import java.util.Scanner;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class NaiveBayes {

	static int[][][] cond = new int[10][10][10];
	static int[] count = new int[4];
	static DecimalFormat df4 = new DecimalFormat("#0.0000");
	public static void Training(int n,XSSFSheet sheet) {
		int rowStart = 1;
		int rowEnd = n;
		int[] a = new int[10];
		for(int i=rowStart;i<=rowEnd;i++) {
			Row r = sheet.getRow(i);
			for(Cell c : r) {	
				a[c.getColumnIndex()] = (int) c.getNumericCellValue();
			}
			for(int j=0;j<=5;j++) {
				cond[j][a[j]][a[5]]++; 
			}	
			count[a[5]]++;
		}
		for(int i=1;i<=3;i++){
			System.out.print(df4.format(lp(i,n))+" ");
		}
		System.out.println();
		System.out.println();
		for(int i=1;i<=5;i++) {
			for(int k=1;k<=3;k++) {
				for(int j=1;j<=4;j++) {
					System.out.print(df4.format(lpcond(i,j,k,n))+" ");
				}
				System.out.println();
			}
			System.out.println();
		}
	}
	public static void Test(int n,XSSFSheet sheet,int T) {
		int rowStart = 1001-n;
		int rowEnd = 1000;
		double correctcount = 0;
		double truepositive = 0,falsepositive = 0,falsenegative = 0;
		int[] a = new int[10];
		for(int i=rowStart;i<=rowEnd;i++) {
			Row r = sheet.getRow(i);
			for(Cell c : r) {	
				a[c.getColumnIndex()] = (int) c.getNumericCellValue();
			}
			
			double sum;
			double ans = 10000;
			int predict = 0;
			for(int v=1;v<=3;v++) {
				sum = 0;
				for(int j=1;j<=5;j++) {
					sum += lpcond(j,a[j-1],v,T);
				}
				sum += lp(v,T);
				if(sum < ans) {
					ans = sum;
					predict = v;
				}
			}
			if(predict == a[5]) {
				correctcount ++;
			}
			
			if(predict == a[5] && a[5] == 3) {
				truepositive ++;
			}
			else if(predict == 3 && a[5] != 3) {
				falsepositive ++;
			}
			else if(predict != 3 && a[5] == 3) {
				falsenegative ++;
			}
		}
		double pre = 0;
		double rec = 0;
		double ac = (correctcount)/(n);
		if(truepositive != 0) {
			pre = truepositive/(truepositive + falsepositive);
			rec = truepositive/(truepositive + falsenegative);
		}
		System.out.print("Accuracy = <"+df4.format(ac)+">  ");
		System.out.print("Precision = <"+df4.format(pre)+">  ");
		System.out.println("Recall = <"+df4.format(rec)+">");
	}
	public static double log2(double x) {//compute the logarithm base 2 of x
		return Math.log(x)/Math.log(2);
	}
	public static double lp(int v,int T) {    //logarithm probability of X.a6 = v
		double p = log2((count[v]+0.1)/(T+0.3));
		return -p;
	}
	public static double lpcond(int i,int u,int v,int T) { //lp(X.ai=u|X.a6=v)
		double p;
		p = log2((cond[i-1][u][v]+0.1)/(count[v]+0.4));
		return -p;
	}
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		InputStream ExcelFile = new FileInputStream("C:\\Users\\Public\\test2.xlsx");
		
		
		XSSFWorkbook W = new XSSFWorkbook(ExcelFile);
		XSSFSheet sheet = W.getSheetAt(0);
		
		Scanner in = new Scanner(System.in);
		int x = in.nextInt();
		int y = in.nextInt();
		Training(x,sheet);	
		Test(y,sheet,x);
	}
}
