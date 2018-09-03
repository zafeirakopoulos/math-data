import java.util.Scanner;

public class Test {
    public static void main(String [] args){
        Scanner reader = new Scanner(System.in);  // Reading from System.in
        System.out.println("Welcome to GraphData!");
        System.out.print("Please enter an id to create a new graph (id should be an integer value): ");
        int graphId = reader.nextInt();
        Graph graph = new Graph(graphId);
        System.out.println("Graph " + graph.getId() + " is created.");
        System.out.print("Please decide how many nodes will be created in the graph (the value should be integer): ");
        int nodeSize = reader.nextInt();
        graph.addNode(nodeSize);
        System.out.println(graph.getNodes().size() + " nodes are created in the graph. Their ids are between 0 and " + (nodeSize-1));
        System.out.println("Please add edges to the graph. In order to create an edge, you should add startNodeId endNodeId isDirected(true or false).\nIf you want to quit to add new edges, you can enter \"quit\".Otherwise you can continue to add new edges.");
        String edge = "";
        while (!edge.equals("quit")){
            System.out.print("Add new edge: ");
            edge = reader.nextLine();
            if(!edge.isEmpty()){
                if (edge.equals("quit"))
                    System.out.println("Adding edges is finished.");
                else{
                    String [] elements = edge.split(" ");
                    System.out.println(graph.addEdge(Integer.parseInt(elements[0]), Integer.parseInt(elements[1]), Boolean.parseBoolean(elements[2])));
                }
            }

        }

        System.out.println();

    }
}
