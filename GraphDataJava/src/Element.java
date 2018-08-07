import java.util.HashMap;

public class Element {
    private int id;
    private HashMap<String, String> attributes;

    public Element(int id) {
        this.id = id;
        this.attributes = new HashMap<>();
    }

    public void addAtrributes(String name, String value){
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
