
public class key {

	int index;
	String str;
	int num;
	String tf;
	public key(int index, String str) {
		// TODO Auto-generated constructor stub
		this.index = index;
		this.str = str;
	}
	public key(int index,String str,int num) {
		this.index = index;
		this.str = str;
		this.num = num;
	}
	public void print() {
		System.out.println(index+" "+str);
	}
}
