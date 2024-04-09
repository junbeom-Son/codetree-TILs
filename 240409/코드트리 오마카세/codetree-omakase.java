import java.util.*;
import java.io.*;

public class Main {

	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st = new StringTokenizer(br.readLine(), " ");
		int L = Integer.parseInt(st.nextToken());
		int Q = Integer.parseInt(st.nextToken());
		Map<String, Queue<Sushi>> sushies = new HashMap<>();
		Map<String, Person> arrivedPeople = new HashMap<>();
		Set<String> names = new HashSet<>();
		StringBuilder answer = new StringBuilder();
		for (int i = 0; i < Q; ++i) {
			st = new StringTokenizer(br.readLine(), " ");
			int command = Integer.parseInt(st.nextToken());
			int time = Integer.parseInt(st.nextToken());
			if (command == 100) {
				int number = Integer.parseInt(st.nextToken());
				String name = st.nextToken();
				putSushi(name, number, time, sushies);
			} else if (command == 200) {
				int number = Integer.parseInt(st.nextToken());
				String name = st.nextToken();
				int foodCount = Integer.parseInt(st.nextToken());
				arrivedPeople.put(name, new Person(time, number, foodCount));
				names.add(name);
			} else {
				takePhoto(answer, time, sushies, arrivedPeople, L, names);
			}
		}
		br.close();
		System.out.print(answer.toString());
	}
	
	private static void takePhoto(StringBuilder answer, int time, Map<String, Queue<Sushi>> sushies,
			Map<String, Person> arrivedPeople, int L, Set<String> names) {
		int leftSushiCount = 0;
		List<String> removeNames = new ArrayList<>();
		for (String name : names) {
			Person person = arrivedPeople.get(name);
			if (!sushies.containsKey(name)) {
				continue;
			}
			int haveCount = sushies.get(name).size(); // 먹기 전 회전판 위에 있는 초밥 수
			haveSushies(time, L, sushies.get(name), person);
			person.foodCount -= haveCount - sushies.get(name).size();
			if (person.foodCount == 0) { // 먹어야 되는 초밥 수를 다 먹었다면 스시, 도착 사람 삭제
				removeNames.add(name);
			}
		}
		for (String name : removeNames) {
			sushies.remove(name);
			arrivedPeople.remove(name);
			names.remove(name);
		}
		for (String name : sushies.keySet()) {
			leftSushiCount += sushies.get(name).size();
		}
		answer.append(arrivedPeople.size()).append(" ").append(leftSushiCount).append("\n");
	}

	private static void haveSushies(int time, int L, Queue<Sushi> sushies, Person person) {
		Queue<Sushi> leftSushies = new LinkedList<>();
		while (!sushies.isEmpty()) {
			Sushi sushi = sushies.poll();
			if (!canHaveSushi(time, L, sushi, person)) {
				leftSushies.add(sushi);
			}
		}
		
		sushies.addAll(leftSushies);
	}
	
	private static boolean canHaveSushi(int photoTime, int L, Sushi sushi, Person person) {
		int rotateTime = (person.time - sushi.time) % L;
		int sushiIndex = (sushi.number + rotateTime) % L;
		int personIndex = person.number;
		if (personIndex < sushiIndex) {
			personIndex += L;
		}
		int arriveTime = person.time + (personIndex - sushiIndex);
		if (arriveTime <= photoTime) { // 사진찍는 시간보다 사람이 있는 위치에 도착하는 시간이 더 빠르면
			return true;
		}
		return false;
	}

	private static void putSushi(String name, int number, int time, Map<String, Queue<Sushi>> sushies) {
		if (!sushies.containsKey(name)) {
			sushies.put(name, new LinkedList<>());
		}
		sushies.get(name).add(new Sushi(time, number));
	}
}

class Sushi {
	int time;
	int number;
	public Sushi(int time, int number) {
		this.time = time;
		this.number = number;
	}
}

class Person {
	int time;
	int number;
	int foodCount;
	public Person(int time, int number, int foodCount) {
		this.time = time;
		this.number = number;
		this.foodCount = foodCount;
	}
}