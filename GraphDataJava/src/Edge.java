import java.util.HashMap;
import java.util.SplittableRandom;

public class Edge extends Element {
    private Node startNode;
    private Node endNode;
    private boolean directed;

    public Edge(int id, Node startNode, Node endNode, boolean directed) {
        super(id);
        this.startNode = startNode;
        this.endNode = endNode;
        this.directed = directed;
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
