""" 
Marcus Sandri
Universidade Federal de Sao Carlos

Este codigo monta a topologia fora do Handle_PacketIn() e 

v. Beta 1.0

"""
#import matplotlib.pyplot as plt
#from collections import *
import networkx as nx
#import numpy as np
#import matplotlib.pyplot as plt
#import pylab
#import itertools
#import hashlib as hash

#log = core.getLogger()

G = nx.DiGraph() # Inicia G

switch_list = list()
switch_list = [[4, 1, 2, 2], [4, 2, 3, 2], [3, 1, 1, 3], [3, 2, 4, 2], [1, 3, 3, 1], [1, 2, 2, 1], [2, 1, 1, 2], [2, 2, 4, 1], [1, 3, 3, 1], [2, 1, 1, 2], [1, 2, 2, 1], [3, 1, 1, 3], [2, 2, 4, 1], [4, 1, 2, 2], [4, 2, 3, 2], [3, 2, 4, 2]]



#vertex = [1,2,3,4,5]
#edges = [[1, 2], [2, 1], [1, 4],[4, 1], [1, 3],[3, 1], [4, 3], [2, 3], [2, 3], [4, 2], [5, 3], [3, 5], [4, 5], [5, 4]]

def rem_repeated_links(input):
    #TODO: Remove XXXX and add the Class name
    """
    When XXXX listen 'openflow-dicovery' module, it
    listen also repeated values. This function remove 
    those values.
    """
    output = []
    for x in input:
      if x not in output:
        output.append(x)
    return output
	
def remove_value(search, input):
  """
  This function is used to remove values in a list. 
  We use it @ 'rem_repeated_links' 
  """
    
  output = []
  for x in input:
    output.append(x)
    if search in output:
      output.remove(x)
  return output

def all_disjointed_paths(vertex, edge, src, dst):
    """
    This function returns all_di(sjointed_paths
    Use: all_disjointed_paths(vertx,edge,source,destination)
    Will return all shortest and disointed paths between
    """
    all_paths = list()
    G.clear()
    G.add_nodes_from(vertex) # colocar vertice no lugar de new_list
    G.add_edges_from(edge) # colocar aresta no lugar de edge
    [[all_paths.append(i)] for i in nx.all_shortest_paths(G,src,dst)] # pretty! 
    return all_paths




def filter_edge_vertex(switch_list):
  #TODO: Translate the function to be used with constructor
  """ 
  This function is used for desassembly
  a graph G(V,E). Then, it will be used in
  all_disjointed_paths()
  
  Use: filter_edge_vertex(list of switches)
  Will return: edge and vertex
  """
  
  temporary_edge = list()
  temporary_vertex = list()

  for i in switch_list:
        temporary_edge.append((i[0], i[2]))
  edge = rem_repeated_links(temporary_edge) 

  for i in switch_list:
        temporary_vertex.append(i[0])
  vertex = rem_repeated_links(temporary_vertex) 
  return edge, vertex


def swport_to_node(paths, switch_list):
  """
  This function is used for joint all 
  switchports with some node
  
  Use: swport_to_node(given path, list of
  switches)
  """
  def bucket(input, value):
    return filter(lambda x: x[0] == value, input)
  #TODO: USE LIST COMPREHENSION  
  sw = rem_repeated_links(switch_list)
  node = dict()
  for i in paths:
    fil = bucket(sw, i)
    node[i] = fil
  return node







# Filtered values
filtered_sw = filter_edge_vertex(switch_list) 
edges = filtered_sw[0]
vertex = filtered_sw[1]

# Shortest paths 
shortest_paths = all_disjointed_paths(vertex, edges, 1, 4)
#print "Shortest-paths", shortest_paths 


# JOIN NODES WITH SWITCHPORT  
paths = shortest_paths[0]
#[swport_to_node(i, switch_list) for i in shortest_paths]
virtual_topology = list()
for i in shortest_paths:
  virtual_topology.append(swport_to_node(i, switch_list))


# Parsing rules

#XXX: Its working fine!

for j in virtual_topology:
  keys = j.keys()
  print "\n"
  for i in keys:
    raw = j.get(i)
    for k in raw:
      print k
      for g in k:
        print g # for i in shortest_paths:
 
