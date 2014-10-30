""" 
Marcus Sandri
Universidade Federal de Sao Carlos

Este codigo monta a topologia fora do Handle_PacketIn() e 

v. Beta 1.0

"""
import matplotlib.pyplot as plt
from collections import *
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import itertools
import hashlib as hash

#log = core.getLogger()

G = nx.DiGraph() # Inicia G
switches = {}

class Auxiliar(object):
  """ Auxiliar e usada para guardar os metodos a serem utilizados. """


  def __init__ (self):
    self.test = None
	
  def uniq(self, input):
  # Funcao retira valores repetidos da lista.
  # Entra com lista inteira e retorna lista sem 
  # valores repetidos

    output = []
    for x in input:
      if x not in output:
        output.append(x)
    return output
	

  def del_val(self, search, input):
  # Funcao deleta valores da lista
  # del_val(valor_a_ser_deletado, lista)

    output = []
    for x in input:
      output.append(x)
      if search in output:
        output.remove(x)
    return output

  def grafo(self, vertice, aresta, src, dst):
  # Funcao retorna menor caminho
  # Entra com: grafo(vertice,aresta,origem,destino)
  # Ira retornar o menor caminho calculado por Dijkstra

    G.clear()
    G.add_nodes_from(vertice) # colocar vertice no lugar de new_list
    G.add_edges_from(aresta) # colocar aresta no lugar de edge
    return nx.dijkstra_path(G,src,dst)
 

  
  






aux = Auxiliar()
k = list()
k = [[4,3,3,2],[2,3,3,4],[2,3,3,1],[4,2,2,1]]

matriz = aux.uniq(k) # matriz sem os valores repetidos
vertex = list()
edges = list()

for i in matriz:
  vertex.append(i[0])
  edges.append(aux.uniq((i[0],i[3])))

print "vertex", aux.uniq(vertex)
print "edge", edges

print "shortest-path", aux.grafo(aux.uniq(vertex), edges, 2, 4)


 ###### Working on this function #######

"""for i in xrange(0,len(k)):
  item = k.__getitem__(i)
  has_item = item.count(4)
  if has_item == 1:
    new_list = list()
    new_list.append(item)
    print new_list
k = aux.del_val(item, k)
print k    
"""
def new_topology(topo, sws):
  # Funcao retorna nova topologia 
  # new_topology(topologia, switch a ser removido)
  for i in xrange(0,len(topo)):
    if topo[i][0] != sws:
      new_list = list()
      new_list.append(topo[i])
  return new_list


print new_topology(k,4)




