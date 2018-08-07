import java.util.HashMap;
import java.util.HashSet;

public class Node {
    private int id;
    private HashMap<String, String> attributes;
    public Node(int id) {
        this.id = id;
        this.attributes = new HashMap<>();
    }

    public void addAttribute(String name, String value){
        if(this.attributes.containsKey(name)){
            this.attributes.computeIfPresent(name, (k, v) -> value);
        }
        else {
            this.attributes.put(name, value);
        }
    }

    public int getId() {
        return id;
    }

    public HashMap<String, String> getAttributes() {
        return attributes;
    }
}
