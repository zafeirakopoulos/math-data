import java.util.ArrayList;
import java.util.HashMap;

public class Graph {
    private ArrayList<Node> nodes;
    private ArrayList<Edge> edges;
    private HashMap<String, String> features;
    private static int nodeId;
    private static int edgeId;

    public Graph() {
        this.nodes = new ArrayList<>();
        this.edges = new ArrayList<>();
        this.features = new HashMap<>();
    }

    public void addNode(){
        Node newNode = new Node(nodeId);
        this.nodes.add(newNode);
        nodeId++;
    }

    public void addEdge(Node startNode, Node endNode, boolean directed){
        if (this.nodes.contains(startNode) && this.nodes.contains(endNode)) {
            Edge newEdge = new Edge(edgeId, startNode, endNode, directed);
            this.edges.add(newEdge);
            edgeId++;
        }
    }

    public void addFeature(String name, String value){
        if (this.features.containsKey(name)){
            this.features.computeIfPresent(name, (k, v) -> value);
        }
        else {
            this.features.put(name, value);
        }
    }

    public ArrayList<Node> getNodes() {
        return nodes;
    }

    public ArrayList<Edge> getEdges() {
        return edges;
    }

    public HashMap<String, String> getFeatures() {
        return features;
    }
}
