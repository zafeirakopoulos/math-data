from graph import Graph

def main():

	print("Welcome to GraphData!")
	graphid = None

	while type(graphid) is not int:
	   try:
	      graphid = input("Please enter an id to create a new graph (id should be an integer value): ")
	      graphid = int(graphid)  
	   except ValueError:
	      print("It is not integer.Please try again")

	gr = Graph(graphid)
	print("Graph " + str(gr.get_id()) + " is created.")

	nodesize = None
	while type(nodesize) is not int:
	   try:
	      nodesize = input("Please decide how many nodes will be created in the graph (the value should be integer): ")
	      nodesize = int(nodesize)  
	   except ValueError:
	      print("It is not integer.Please try again")

	gr.add_nodes(nodesize)
	print(str(len(gr.get_nodes())) + " nodes are added. Their ids are between " + str(0) + " and " + str((nodesize - 1)))
	print("Please add edges to the graph. In order to create an edge, you should add startNodeId endNodeId isDirected(true or false).\nIf you want to quit to add new edges, you can enter \"quit\".Otherwise you can continue to add new edges.")
	edge = ""

	while edge != "quit":
		edge = input("Add new edge: ")
		
		if(not edge is ""):
			if(edge == "quit"):
				print ("Adding edges is finished.")
			else:
				elements = []
				elements = edge.split(' ')
				if len(elements) == 3:
					answer = gr.add_edges(int(elements[0]) , int(elements[1]), int(elements[2]))
					print(answer)
				else:
					print("lLst index out of range")
				

				
		
main()


