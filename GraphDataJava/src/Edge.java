import java.util.HashMap;
import java.util.SplittableRandom;

public class Edge {
    private int id;
    private HashMap<String, String> attributes;
    private Node startNode;
    private Node endNode;
    private boolean directed;

    public Edge(int id, Node startNode, Node endNode, boolean directed) {
        this.id = id;
        this.startNode = startNode;
        this.endNode = endNode;
        this.directed = directed;
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

    public Node getStartNode() {
        return startNode;
    }

    public Node getEndNode() {
        return endNode;
    }

    public boolean isDirected() {
        return directed;
    }
}
