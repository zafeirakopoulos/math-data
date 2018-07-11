import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.implementations.SingleGraph;

import java.util.TreeMap;

public class Main {
    public static void main(String [] args){
        Graph graph = new SingleGraph("Gizem");
        TreeMap<String, String > attributes = new TreeMap<>();
        attributes.put("density", "15");
        attributes.put("Nodes", "10");
        MdGraphGenerator generator = new MdGraphGenerator("Random", graph, attributes);
        System.out.println(generator.generateGraph());
        System.out.println(graph.getNodeCount());
    }
}
