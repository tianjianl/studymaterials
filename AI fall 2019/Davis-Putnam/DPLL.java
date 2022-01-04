import java.util.ArrayList;
import java.util.Scanner;

public class DPLL {
	static int max,cnt = 0;
	static int number;
	//max = number of atoms cnt = number of clauses
	public static boolean[] deleted = new boolean[10005];
	public static ArrayList<Integer>[] Clause = new ArrayList[10005];
	//S := set of clauses, number := number of clauses need to be done
	public static ArrayList<Integer>[] Clone(ArrayList<Integer>[] s) {
		ArrayList<Integer>[] New = new ArrayList[10005];
		for(int i=1;i<=cnt;i++) {
			New[i] = new ArrayList<Integer>(s[i]);
		}
		return New;
	}
	public static void PrintClauses(ArrayList<Integer>[] S) {
		System.out.println("begin printing clauses");
		for(int i=1;i<=cnt;i++) {
			ArrayList<Integer>[] Sp = Clone(S);
			while(Sp[i].isEmpty() == false) {
				System.out.print(Sp[i].remove(0)+" ");
			}
			System.out.println();
		}
	}
	public static void PrintAnswer(int[] atom)
	{
		for(int i=1;i<=max;i++) {
			if(atom == null)
			System.out.println("No solution");
			else if(atom[i] == 1)
			System.out.println(i+" T");
			else if(atom[i] == 0)
			System.out.println(i+" F");
		}
	}
	public static boolean CheckAnswer(ArrayList<Integer>[] S,boolean d[]) {
		for(int i=1;i<=cnt;i++) {
			if(S[i].size() == 0 && d[i] == false) {
				return false;
			}
		}
		return true;
	}
	public static boolean Check(ArrayList<Integer>[] S) {
		int[] flag = CheckLiteral(S);
		/*for(int i=1;i<=max;i++) {
			System.out.println(i+" "+flag[i]);
		}*/
		for(int i=1;i<=max;i++) {
			if(flag[i] == 1 || flag[i] == -1 ) {
				return true;
			}
		}
		return false;
	}
	public static boolean Check2(ArrayList<Integer>[] S) {
		for(int i=1;i<=cnt;i++) {
			if(S[i].size() == 1) {
				return true;
			}
		}
		return false;
	}
	private static boolean CheckFinal(ArrayList<Integer>[] s, boolean[] d) {
		// TODO Auto-generated method stub
		for(int i=1;i<=cnt;i++){
			if(d[i] == false)
				return false;
		}
		return true;
	}
	public static int[] CheckLiteral(ArrayList<Integer>[] S) {
		boolean[] haspositive = new boolean[max+5];
		boolean[] hasnegative = new boolean[max+5];
		for(int i=1;i<=max;i++) {
			haspositive[i] = hasnegative[i] = false;
		}
		for(int i=1;i<=cnt;i++) {
			for(int j=1;j<=max;j++){
				if(S[i].contains(j))
					haspositive[j] = true;
				if(S[i].contains(-j))
					hasnegative[j] = true; 
			}
		}
		int[] isliteral = new int[max+5];
		for(int i=1;i<=max;i++){
			if(haspositive[i] == true && hasnegative[i] == false)
				isliteral[i] = 1;
			else if(haspositive[i] == false && hasnegative[i] == true)
				isliteral[i] = -1;
			else
				isliteral[i] = 0;
		}
		return isliteral;
	}
	private static void propagate(int temp, int[] a, ArrayList<Integer>[] s,boolean[] d) {
		for(int i=1;i<=cnt;i++){
			
			if(a[temp] == 1 && s[i].contains(temp)) {
				s[i].clear();
				d[i] = true;
			}
			else if(a[temp] == 0 && s[i].contains(-temp)) {
				s[i].clear();
				d[i] = true;
			}
			
			else if(a[temp] == 0 && s[i].contains(temp)) {
				int index = s[i].indexOf(temp);
				s[i].remove(index);
			}
			else if(a[temp] == 1 && s[i].contains(-temp)) {
				int index = s[i].indexOf(-temp);
				s[i].remove(index);
			}  
		  }
	//PrintClauses(s);
	}
	public static int[] dp(ArrayList<Integer>[] S,int[] A,boolean[] d) {
		while(true) {
		if(CheckFinal(S,d) == true) {
			//all clauses are satisfied
			for(int i=1;i<=max;i++) {
				if(A[i] == -1) {
					A[i] = 1;
				}
			}
			return A;
		}
		else if(CheckAnswer(S,d) == false) {
			return null;
		}
		
		else if(Check(S) == true){
			int[] literal = CheckLiteral(S);
			for(int i=1;i<=max;i++) {
				if(literal[i] == 1 && A[i] == -1) {
					A[i] = 1; //true
					//System.out.println("assigned true to "+i);
					for(int j=1;j<=cnt;j++) { //find all containing the literal i and delete
						if(S[j].contains(i)) {
							S[j].clear();
							d[j] = true;
						}
					}
				}
				else if(literal[i] == -1 && A[i] == -1){
					A[i] = 0; //false
					//System.out.println("assigned false to "+i);
					for(int j=1;j<=cnt;j++) { //find all containing the literal -i and delete
						if(S[j].contains(-i)) {
							S[j].clear();
							d[j] = true;
						}
					}
		     	}
			}
			//PrintClauses(S);
		}
		else if(Check2(S) == true) {
			for(int i=1;i<=cnt;i++) {
				if(S[i].size() == 1) {
					int temp = S[i].get(0);
					if(temp < 0 && A[-temp] == -1) {
						A[-temp] = 0; //false
						//System.out.println("assigned false to "+-temp);
						propagate(-temp,A,S,d);
					}
					else if(temp > 0 && A[temp] == -1){
						A[temp] = 1; //true
						//System.out.println("assigned true to "+temp);
						propagate(temp,A,S,d);
					}
				}
			}
		}
		else 
			break;
	}
	//hard cases
	int temp = 0;
	int[] A1 = new int[max+5];
	for(int i=1;i<=max;i++) {
		A1[i] = A[i];
	}
	boolean[] D1  = new boolean[cnt+5];
	for(int i=1;i<=cnt;i++) {
		D1[i] = d[i];
	}
	
	for(int i=1;i<=max;i++) {
		if(A[i] == -1){
			A1[i] = 1;
			//System.out.println("assigned true to "+i);
			temp = i;
			break; //choose the first unassigned atom and assign it to one
		}
	}
	ArrayList<Integer>[] S1 = new ArrayList[10005];
	S1 = Clone(S);
	propagate(temp,A1,S1,D1);
	int[] Anew = dp(S1,A1,D1);
	if(Anew != null)
		return Anew;
	else {
		int[] A2 = new int[max+5];
		for(int i=1;i<=max;i++) {
			A2[i] = A[i];
		}
		boolean[] D2 = new boolean[cnt+5];
		for(int i=1;i<=cnt;i++) {
			D2[i] = d[i];
		}
		
		A2[temp] = 0;
		//System.out.println("reassigned false to "+temp);
		S1 = Clone(S);
		propagate(temp,A2,S1,D2);
		return dp(S1,A2,D2);
	}
}

	public static void main(String[] args) {
		
		Scanner in = new Scanner(System.in);
		for(int i=1;i<=10000;i++) {
			Clause[i] = new ArrayList<Integer>();
		}
		
		//input of clauses
		while(in.hasNextLine()) {
			cnt++;
			String s = in.nextLine();
			String[] str = s.split(" ");
			int[] a = new int[str.length];
			if(Integer.parseInt(str[0]) == 0)
				break;
			for(int i=0;i<str.length;i++){
				a[i] = Integer.parseInt(str[i]);
				if(a[i] > max)
					max = a[i];
				Clause[cnt].add(a[i]);
			}
		}
		
		cnt--;
		
	
		int[] atom = new int[max+5];
		
		//initializations
		for(int i=1;i<=max;i++){
			atom[i] = -1;
		}
		for(int i=1;i<=cnt;i++) {
			deleted[i] = false;
		}
		/* 
		   -1 means unbounded 
			0 means false 
			1 means true
		*/
		//dpll 
		number = cnt;
		System.out.println();
		atom = dp(Clause,atom,deleted);
		for(int i=1;i<=max;i++) {
			if(atom == null)
			System.out.println("No solution");
			else if(atom[i] == 1)
			System.out.println(i+" T");
			else if(atom[i] == 0)
			System.out.println(i+" F");
		}
		System.out.println("0");
		for(int i=1;i<=max;i++) {
			String S = in.nextLine();
			System.out.println(S);
		}
	}
}
