import org.graphstream.algorithm.generator.DorogovtsevMendesGenerator;
import org.graphstream.algorithm.generator.Generator;
import org.graphstream.algorithm.generator.RandomGenerator;
import org.graphstream.graph.Graph;

import java.util.TreeMap;

public class MdGraphGenerator {
    protected Graph graph;
    protected TreeMap<String, String > attributes;
    protected String option;

    public MdGraphGenerator(String option, Graph graph, TreeMap<String, String> attributes) {
        this.graph = graph;
        this.attributes = attributes;
        this.option = option;
    }

    public String generateGraph(){
        if (this.option.equals("Random")){
            return generateGraphRandom();
        }
        return "The option is not found";
    }

    public String generateGraphRandom(){
        String densityString = Util.findAttribute(this.attributes, "density");
        String nodesString = Util.findAttribute(this.attributes, "Nodes");
        if (densityString.equals("Not found") || nodesString.equals("Not found"))
            return "The graph can not be generated.";
        double density = Double.parseDouble(densityString);
        int nodes = Integer.parseInt(nodesString);
        System.out.println("nodes " + nodes + " density : " + density);
        Generator gen = new RandomGenerator(findAverageDegree(density, nodes), false, false);
        gen.addSink(this.graph);
        gen.begin();
        for(int i=0; i<nodes; i++)
            gen.nextEvents();
        gen.end();
        return "The graph is generated successfully";
    }

    public double findAverageDegree(double density, double nodes){
        if (density <= 1.0){
            density *= 100;
        }
        double totalDegree = ((double)(nodes * (nodes-1))/2.0)*density;
        return totalDegree/(double)nodes;
    }

    public String DorogovtsevMendes(){
        String nodesString = Util.findAttribute(this.attributes, "Nodes");
        if (nodesString.equals("Not found"))
            return "The graph can not be generated.";
        int nodes = Integer.parseInt(nodesString);
        Generator gen = new DorogovtsevMendesGenerator();
        gen.addSink(graph);
        gen.begin();

        for(int i=0; i<nodes; i++) {
            gen.nextEvents();
        }
        gen.end();
        return "The graph is generated successfully";
    }




}
