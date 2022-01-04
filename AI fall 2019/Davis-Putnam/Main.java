import java.util.Scanner;

public class Main {

	static int V;
	static String S = "0ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	static int[][] mat = new int[30][30];
	public static void PrintKey()
	{
		System.out.println("0");
		for(int i=1;i<=V;i++)
			for(int j=1;j<=V;j++) {
				System.out.println((i-1)*V+j+" "+S.charAt(i)+" "+j);
			}
	}
	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		V = in.nextInt();
		for(int i=0;i<=29;i++)
			for(int j=0;j<=29;j++) {
				mat[i][j] = 0;
			}
		
		while(in.hasNext())
		{
			String u = in.next();
			String v = in.next();
			mat[S.indexOf(u)][S.indexOf(v)] = 1;
		}
		
		for(int i=1;i<=V*V;i++) {
			System.out.print(i+" ");
			if(i%4 == 0)
				System.out.println();
		}
		
		for(int i=1;i<=V*V;i++)
			for(int j=i+V;j<=V*V;j=j+V){
				if(j <= V*V)
					System.out.println("-"+i+" "+"-"+j);
			}
		
		for(int i=1;i<=V;i++)
			for(int j=1;j<=V;j++){
				if(mat[i][j] == 0 && i!=j) {
					//System.out.println(i+" "+j);
					for(int t=1;t<V;t++) {
						int u = (i-1)*V+t;
						int v = (j-1)*V+t+1;
						System.out.println("-"+u+" "+"-"+v);
					}
				}
			}
		//optional
		for(int i=1;i<=V;i++) {
			for(int j=1;j<=V;j++) {
				int u = (j-1)*V+i;
				System.out.print(u+" ");
			}
			System.out.println();
		}
		
		for(int i=1;i<=V;i++) {
			for(int s=1;s<=V;s++)
				for(int t=s+1;t<=V;t++) {
					int u = (i-1)*V+s;
					int v = (i-1)*V+t;
					System.out.println("-"+u+" "+"-"+v);
				}
		}
		PrintKey();
	}
}
