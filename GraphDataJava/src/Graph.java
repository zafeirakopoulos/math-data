import java.util.ArrayList;
import java.util.HashMap;

public class Graph extends Element {
    private ArrayList<Node> nodes;
    private ArrayList<Edge> edges;
    private static int nodeId;
    private static int edgeId;

    public Graph(int id) {
        super(id);
        this.nodes = new ArrayList<>();
        this.edges = new ArrayList<>();
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

    public ArrayList<Node> getNodes() {
        return nodes;
    }

    public ArrayList<Edge> getEdges() {
        return edges;
    }

}
