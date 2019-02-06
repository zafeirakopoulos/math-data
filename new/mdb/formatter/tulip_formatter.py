from tulip import tlp
from tulipgui import tlpgui
import json

graph = tlp.loadGraph("graphtlp.tlp")
for n in graph.getNodes():
  degree = graph.deg(n)
  print("the degree of", n, "is", degree)

tlp.saveGraph(graph, 'graph.svg')
