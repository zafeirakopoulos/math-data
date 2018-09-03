import java.util.ArrayList;
import java.util.HashMap;

public class Graph extends Element {
    private ArrayList<Node> nodes;//json
    private ArrayList<Edge> edges;//json
    private static int nodeId;//functional
    private static int edgeId;//functional

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

    public void addNode(int nodeSize){
        for (int i = 0; i < nodeSize ; i++) {
            addNode();
        }
    }

    public String addEdge(int startNodeId, int endNodeId, boolean directed){
        int nodeSize = this.nodes.size();
        if (startNodeId < nodeSize && endNodeId < nodeSize) {
            Node startNode = getNodeById(startNodeId);
            Node endNode = getNodeById(endNodeId);
            if (directed){
                if(searchIfExistDirected(startNode, endNode))
                    return "The directed edge has already existed.";
            }
            else{
                if(searchIfExistUndirected(startNode, endNode))
                    return "The undirected edge has already existed.";
            }

            Edge newEdge = new Edge(edgeId, startNode, endNode, directed);
            this.edges.add(newEdge);
            edgeId++;
            return "The new edge between " + startNodeId + " and " + endNodeId + " is added with " + newEdge.getId() + " id.";

        }
        else {
            return "Start node and/or end node do/does not contain in the graph. Please try another node(s).";
        }
    }

    public ArrayList<Node> getNodes() {
        return nodes;
    }

    public ArrayList<Edge> getEdges() {
        return edges;
    }

    public Node getNodeById(int id){
        return this.nodes.get(id);
    }

    public boolean searchIfExistDirected(Node startNode, Node endNode){
        for (Edge edge: this.edges) {
            if (edge.getStartNode().equals(startNode) && edge.getEndNode().equals(endNode)){
                return true;
            }
        }
        return false;
    }

    public boolean searchIfExistUndirected(Node startNode, Node endNode){
        for (Edge edge: this.edges) {
            if (edge.getStartNode().equals(startNode) && edge.getEndNode().equals(endNode)){
                if (!edge.isDirected())
                    return true;
            }
            else if(edge.getStartNode().equals(endNode) && edge.getEndNode().equals(startNode)){
                if(!edge.isDirected())
                    return true;
            }
        }
        return false;
    }

}
