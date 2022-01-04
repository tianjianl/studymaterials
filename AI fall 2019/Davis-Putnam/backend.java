import java.util.Scanner;

public class backend {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner in = new Scanner(System.in);
		boolean[] arr = new boolean[255];
		String[] printarr = new String[255];
		int max = 0;
		for(int i=1;i<=250;i++) {
			arr[i] = false;
		}
		int cnt = 0;
		while(in.hasNextLine()) {
			int index = in.nextInt();
			if(index == 0) {
				break;
			}
			cnt++;
			String flag = in.next();
			if(flag.equals("T")) {
				arr[index] = true;
			}
		}
		for(int i=1;i<=cnt;i++) {
			int index = in.nextInt();
			String A = in.next();
			int time = in.nextInt();
			if(arr[index] == true) {
				printarr[time] = A;
			}
			if(time > max)
				max = time;
		}
		for(int i=1;i<max;i++) {
			System.out.print(printarr[i]+"->");
		}
		System.out.println(printarr[max]);
	}
}

