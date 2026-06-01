import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Scanner;
import java.util.Set;
import java.util.stream.Collectors;

public class PCY {
	
	public static void main(String[] args) {
		
		List<List<String>> basketi = new ArrayList<>();
		int N = 0, b = 0;
		Double s = 0.0;

		Map<String, Integer> freq = new HashMap<>();
		Map<String, Double> support = new HashMap<>(); // u koliko kosarica se pojavljuje
		
		int idx = 0;
		try(Scanner sc = new Scanner(System.in)){
			while(sc.hasNextLine()) {
				String linija = sc.nextLine();
				
				if(idx == 1) s = Double.parseDouble(linija);
				else if(idx == 0) N = Integer.parseInt(linija);
				else if(idx == 2) b = Integer.parseInt(linija);
				
				else{
					List<String> items_u_kosarici = new ArrayList<>(List.of(linija.split(" ")));
					basketi.add(items_u_kosarici);
				}
				idx++;
			}
		} 
		catch(Exception e) {
			System.out.println("Greska u citanju: " + e);
		}


		final double brojKosarica = N * 1.;
		final double prag = s * brojKosarica;
		final int brojPretinaca = b;
		ArrayList<Integer> pretinci = new ArrayList<>(Collections.nCopies(brojPretinaca, 0));

		// prvi prolaz, pobroji koliko u koliko se kosara pojedini element pojavljuje
		for(List<String> basket : basketi){
			List<String> elementi_u_tom_retku = new ArrayList<>();
			for(int i = 0; i < basket.size(); i++){
				String item = basket.get(i);
				if(!elementi_u_tom_retku.contains(item)){
					elementi_u_tom_retku.add(item);
					support.merge(item, 1., Double::sum);
				}
			}	
		}

		long temp_A = support.values().stream()
		    .filter(val -> val >= prag)
		    .count();

		long A = temp_A * (temp_A - 1) / 2;
		//System.out.println("Prag" + prag);
		Set<String> setZaP = new HashSet<>();
		// izracunaj support za sve te frekvencije po retcima
		// support.replaceAll((k,v) -> v / brojKosarica);
		for(List<String> basket : basketi){
			for(int i = 0; i < basket.size(); i++){
				for(int j = i + 1; j < basket.size(); j++){
					if((support.get(basket.get(i)) >= prag) && (support.get(basket.get(j)) >= prag)){
						int k = ((Integer.parseInt(basket.get(i)) * support.size() + Integer.parseInt(basket.get(j))) % brojPretinaca); // hashiranje u pretince
						pretinci.set(k, pretinci.get(k) + 1);
				}
			}
		}
	} 
		
		for(List<String> basket : basketi){
			for(int i = 0; i < basket.size(); i++){
				String item_1 = basket.get(i);
				for(int j = i + 1; j < basket.size(); j++){
					String item_2 = basket.get(j);
					if(!item_1.equals(item_2) && (support.get(item_1) >= prag) && 
						(support.get(item_2) >= prag)){
							int k = ((Integer.parseInt(basket.get(i)) * support.size() + Integer.parseInt(basket.get(j))) % brojPretinaca);
							
							if(pretinci.get(k) >= prag){
								String key = item_1.compareTo(item_2) <= 0 
								? item_1 + "|" + item_2 
  								: item_2 + "|" + item_1;
								freq.merge(key, 1, Integer::sum);
								setZaP.add(key);
					}
				}
			}
		}
	}

	long P = setZaP.size();
	List<Integer> vrijednostiCestiParova = freq.values().stream()
    .filter(val -> val >= prag)
    .sorted(Comparator.reverseOrder()) 
    .collect(Collectors.toCollection(ArrayList::new));

		
		//freq.forEach((key, value) -> {
    	//	System.out.println("Pair (" + key + ") appears " + value + " times.");
		//});
		//System.out.println();
		//support.forEach((key, value) -> {
    	//	System.out.println("Item (" + key + ") support is: " + (value));
		//});
		//System.out.println(N);
		//System.out.println(s);
		//System.out.println(b);

	System.out.println(A);
	System.out.println(P);
	for(Integer value : vrijednostiCestiParova){
		System.out.println(value);
	}

	//try (PrintWriter writer = new PrintWriter(new FileWriter("rjesenja.txt"))) {
	//    writer.println(A);
	//    writer.println(P);
	//    for (Integer value : vrijednostiCestiParova) {
	//        writer.println(value);
	//    }
	//} catch (IOException e) {
	//    e.printStackTrace();
	//}
	}
}
