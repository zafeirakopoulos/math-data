class Element(object):

	def __init__(self, elementId):

		self.id = elementId
		self.attributes = {}

	def add_attributes(self, name, value):

		if name in self.attributes:
			self.attributes[name] += 1
			self.attributes = dict(zip(name, value))
		else:
			self.attributes = dict(zip(name, value))

	def get_id(self):
		return self.id

	def get_attributes(self):
		return self.attributes


class Node(Element):

	def __init__(self, nodeId):
		super(Node, self).__init__(nodeId)


class Graph(Element):

	def __init__(self,graphId):

		super(Graph, self).__init__(graphId)

		self.nodes = []
		self.edges = []
		self.nodeId = 0
		self.edgeId = 0

	def add_node(self):

		new_node = Node(self.nodeId)
		self.nodes.append(new_node)
		self.nodeId += 1

	def add_nodes(self, node_size):
		i = 0
		while i < node_size:
			i += 1
			self.add_node()

	def add_edges(self, start_node_id, end_node_id, directed):
		
		node_size = len(self.nodes)
		if start_node_id < node_size and end_node_id < node_size:
			
			start_node = self.get_by_id(start_node_id)
			end_node = self.get_by_id(end_node_id)
			if directed is 1:
				
				if self.search_if_exist_directed(start_node, end_node) is 1: 
					return "The directed edge has already existed."
			elif directed is 0:
				if self.search_if_exist_undirected(start_node, end_node) is 1:
					return "The undirected edge has already existed."
			else:
				return "Wrong directed value.Directed must be 1 or 0"	
			new_edge = Edge(self.edgeId, start_node, end_node, directed)
			self.edges.append(new_edge)
			self.edgeId += 1
			
			return "The new edge between " + str(start_node_id) + " and " + str(end_node_id) + " is added with " + str(new_edge.get_id()) + " id."
		else:
			return "Start node and/or end node do/does not contain in the graph. Please try another node(s)."

	def search_if_exist_directed(self, startNode, endNode):
		self.print_edges()
		for edge in self.edges:
			if edge.get_start_node() == startNode and edge.get_end_node()== endNode:
				if edge.is_directed() is 1:
					return 1
			
		return 0

	def search_if_exist_undirected(self, startNode, endNode):
		self.print_edges()
		for edge in self.edges:
			if edge.get_start_node() == startNode and edge.get_end_node()== endNode:
				if edge.is_directed() is not 1:
					return 1
			elif edge.get_start_node() == endNode and edge.get_end_node()== startNode:
				if edge.is_directed() is not 1:
					return 1
		return 0

	def get_nodes(self):
		return self.nodes

	def get_by_id(self, idx):
		return self.nodes[idx]

	def get_edges(self):
		return self.edges

	def print_edges(self):
		for edge in self.edges:
			print(str(edge.get_start_node().get_id()) + " " + str(edge.get_end_node().get_id()) + " " + str(edge.is_directed()) + "\n")


class Edge(Element):

	def __init__(self, edgeId, start_node, end_node, directed):

		super(Edge, self).__init__(edgeId)
		
		self.start_node = start_node
		self.end_node = end_node
		self.directed = directed


	def get_start_node(self):
		return self.start_node

	def get_end_node(self):
		return self.end_node

	def is_directed(self):
		return self.directed

	def get_attributes(self):
		return self.attributes

	

