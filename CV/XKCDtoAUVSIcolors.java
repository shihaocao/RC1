import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;

public class XKCDtoAUVSIcolors {

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub
		Scanner scan = new Scanner(new File("xkcdColors.txt"));
		PrintWriter pw = new PrintWriter(new File("RGB_Colors.txt"));
//		HashSet<String> set = new HashSet<String>();
		HashMap<String,String> map = new HashMap<String,String>();
		map.put("dark green", "green");
		map.put("light green","green");
		map.put("navy blue","blue");
		map.put("dark blue","blue");
		map.put("light blue","blue");
		map.put("teal","blue");
		map.put("cyan","blue");
		map.put("sky blue","blue");
		map.put("maroon","brown");
		map.put("dark purple","purple");
		map.put("dark red","red");
		map.put("magenta","purple");
		map.put("purple","purple");
		map.put("olive","green");
		map.put("gold","yellow");
		map.put("mustard","brown");
		map.put("lime green","green");
		int count = 0;
		while(scan.hasNextLine()){
			String line = scan.nextLine();
			String[] arr = line.split("]");
/*			
 * Puts all distinct colors into a set.
			if(!set.contains(arr[1].trim())){
				System.out.println(arr[1].trim());
				set.add(arr[1].trim());
				count++;
			}
*/
			if(map.containsKey(arr[1].trim())){
				arr[1] = " " + map.get(arr[1].trim());
			}
			String newString = arr[0] + "]" + arr[1];
			pw.println(newString);
		}
		pw.close();
//		System.out.println(count);	
	}
			//dark green -> green
			//light green -> green
			//navy blue -> blue
			//dark blue -> blue
			//light blue -> blue
			//teal -> blue
			//cyan -> blue
			//sky blue -> blue
			//maroon -> brown
			//dark purple -> purple
			//dark red -> red
			//magenta -> purple
			//purple -> purple
			//olive -> green
			//gold -> yellow
			//mustard -> brown
			//lime green -> green
}
