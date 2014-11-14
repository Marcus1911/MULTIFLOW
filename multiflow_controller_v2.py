""" 
Marcus Sandri
Universidade Federal de Sao Carlos (UFSCar)
Federal University of Sao Carlos


This code it is used to link disjoint. 
In special, this branch is used to disjoint 
MP_CAPABLE and MP_JOIN.  

v. Beta 1.2

"""
from pox.core import core
import pox
import pox.lib.packet as pkt
from pox.lib.revent import *
from pox.openflow.discovery import Discovery
from pox.host_tracker import host_tracker
import pox.openflow.libopenflow_01 as of
from collections import *
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pylab
import itertools
import hashlib as hash

G = nx.DiGraph() # Starts the Graph

class BuildTopo(object):
  """ In this class we create methods for correct build topology """

  def __init__ (self):
    self.test = None
	
  def uniq(self, input):
    """
    Funcao retira valores repetidos da lista.
    Entra com lista inteira e retorna lista sem 
    valores repetidos
    """
    output = []
    for x in input:
      if x not in output:
        output.append(x)
    return output
	
  def delete_value(self, search, input):
    """
    Funcao deleta valores da lista
    del_val(valor_a_ser_deletado, lista)
    """
    output = []
    for x in input:
      output.append(x)
      if search in output:
        output.remove(x)
    return output

  def new_topology(self, topo, sws):
    """
    Funcao retorna nova topologia 
    new_topology(topologia, switch a ser removido) 
    """
    newlist = []
    i = 0 
    for i in range(len(topo)):
      if topo[i][0] != sws:     
        newlist.append(topo[i])
    return newlist


  def grafo(self, vertice, aresta, src, dst):
    """
    Funcao retorna menor caminho
    Entra com: grafo(vertice,aresta,origem,destino)
    Ira retornar o menor caminho calculado por Dijkstra
    """
    G.clear()
    G.add_nodes_from(vertice) # colocar vertice no lugar de new_list
    G.add_edges_from(aresta) # colocar aresta no lugar de edge
    return nx.dijkstra_path(G,src,dst)
 

  def _install (self, switch, in_port, match):
    msg = of.ofp_flow_mod()
    msg.match = match
    msg.actions.append(of.ofp_action_output(port = in_port))
    core.openflow.sendToDPID(switch,msg)


class Multiflow(EventMixin):

  """ Happy_Blue e a classe principal. Esta classe eh utilizada 
  como o modulo final utilizado para separar subfluxos. 
  Ela encapsula Auxiliar(), quando utiliza seus metodos."""


  def __init__ (self):
    #self.connection = None
    #self.ports = None
    #self.dpid = None
    #self.timer = None
    self.switch_memo = [] # _handle_LinkEvent()
    self.host_alive = [] # _handle_HostEvent()
    self.a = [] # _handle_LinkEvent()
    self.v = [] # _handle_LinkEvent()
    self.vertex = [] # _handle_LinkEvent()
    self.edge = [] # _handle_LinkEvent()
    self.Hash_table = {'key':'value'} # Hash table deve iniciar no construtor

    def startup ():
      core.openflow.addListeners(self, priority=0)
      core.openflow_discovery.addListeners(self)
      core.host_tracker.addListeners(self)
    core.call_when_ready(startup, ('openflow','openflow_discovery', 'host_tracker'))

  def _handle_LinkEvent (self, event):
    """ This func() handle 'link events', that means: 
        [*] find all switches avaliable;
        [*] Build topology in Pro-Active mode.
    """

    l = event.link
    self.switch_memo.append([l.dpid1,l.port1,l.dpid2,l.port2])
    print l.end[0] #([l.dpid1,l.port1,l.dpid2,l.port2])
    build = BuildTopo()

    """ Used when switch-list assembling """
    
    for i in self.switch_memo:
      self.v.append(i[1])
    self.vertex = build.uniq(self.v)
  
    for i in self.switch_memo:
      self.a.append((i[0], i[2]))
    self.edge = build.uniq(self.a) 

  def _handle_HostEvent (self, event):
    """ Used to show Avalaible Hosts and its port numbers"""
    self.host_alive.append(event.entry) 
    #print event.entry



  def _handle_PacketIn(self, event):
     build = BuildTopo()
     packet = event.parsed
     packet_ipv4 = packet.find('ipv4')
     packet_tcp = packet.find('tcp')
     packet_udp = packet.find('udp')


     if packet.ARP_TYPE:
       #If ARP, forwarding with L2/L3 if avaliable... 
       msg = of.ofp_flow_mod()
       msg.match = of.ofp_match.from_packet(packet)
       msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
       event.connection.send(msg)

     if packet_udp:
       msg = of.ofp_flow_mod()
       msg.match = of.ofp_match.from_packet(packet)
       msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
       event.connection.send(msg)

     if not packet_tcp: return
     if packet_tcp.SYN and packet_tcp.ACK: return
     if packet_tcp.SYN is True:

       def beUnpack(byte):
         """ Converts byte string to integer. Use Big-endian byte order """
         try:
           return sum([ord(b) << (8 * i) for i, b in enumerate(byte[::-1])])
         except:
           return 'impossible to convert'

       for option in packet_tcp.options:
         if isinstance(option, pkt.TCP.mptcp_opt):
           name_option = type(option).__name__ #,vars(option)
           if name_option == 'mp_capable_opt':
             src = packet.src
             dst = packet.dst
             for host in self.host_alive:
                if src == host.macaddr:
                  source = host.dpid, host.port
                  #print "source dpid", source
                elif dst == host.macaddr:
                  destination = host.dpid, host.port
                  #print "destination dpid", destination
             try:
               shortest_path_capable = build.grafo(self.vertex, self.edge, source[0], destination[0])
               print shortest_path_capable
               
               rules = list()
               for i in xrange(0,len(shortest_path_capable)):
                 for j in xrange(0, len(self.switch_memo)):
                 #    print i, sw[j][0]
                   try:
                     if shortest_path_capable[i]  == self.switch_memo[j][0] and shortest_path_capable[i+1] == self.switch_memo[j][2]:
                       print shortest_path_capable[i], [self.switch_memo[j][0], self.switch_memo[j][1]]
                       rules.append([self.switch_memo[j][0],self.switch_memo[j][1]])
                   except:
                     rules.append(list(destination))     
                     print "last switch, adding the host"
 
               # working on this loop
               # Doesn't work quite better yet
               for i in xrange(0, len(shortest_path_capable) + 1):
                 rule_to_switch = rules.pop()
                 
     
               
                 match = of.ofp_match()
                 match.nw_proto=6
                 match.dl_type=0x800
                 match.nw_src = packet_ipv4.srcip
                 match.nw_dst = packet_ipv4.dstip
                 match.tp_src = packet_tcp.srcport
                 match.tp_dst = packet_tcp.dstport
                 _install(rule_to_switch[0], rule_to_switch[1], match)
                 print "forwarding-rule", rule_to_switch
              
                 
                 

               # need reverse path

               
               """
               for i in multiflow_to_switch:
                 msg = of.ofp_flow_mod()
                 msg.match = match
                 msg.actions.append(of.ofp_action_output(port = i[1]))
                 core.openflow.sendToDPID(i[0],msg)
               
                 msg = of.ofp_flow_mod()
                 msg.match = match
                 msg.actions.append(of.ofp_action_output(port = i[3]))
                 core.openflow.sendToDPID(i[2],msg)


               msg = of.ofp_flow_mod()
               msg.match = match
               msg.actions.append(of.ofp_action_output(port = source[1]))
               core.openflow.sendToDPID(source[0],msg)


               msg = of.ofp_flow_mod()
               msg.match = match
               msg.actions.append(of.ofp_action_output(port = destination[1]))
               core.openflow.sendToDPID(destination[0],msg)
               """


             except:
               print 'Waiting paths...'
               return

"""  
             
                    
             # Reverse Match 
           
             rmatch = of.ofp_match()
             rmatch.nw_proto=6
             rmatch.dl_type=0x800
             rmatch.nw_src = packet_ipv4.dstip
             rmatch.nw_dst = packet_ipv4.srcip
             rmatch.tp_src = packet_tcp.dstport
             rmatch.tp_dst = packet_tcp.srcport
             
	     # Path 
             msg = of.ofp_flow_mod()
             msg.match = match
             msg.actions.append(of.ofp_action_output(port = 4))
             core.openflow.sendToDPID(1,msg)
                    
             msg = of.ofp_flow_mod()
             msg.match = match
             msg.actions.append(of.ofp_action_output(port = 2))
             core.openflow.sendToDPID(4,msg)
                  

             # Reverse Path 
             msg = of.ofp_flow_mod()
             msg.match = rmatch
             msg.actions.append(of.ofp_action_output(port = 4))
             core.openflow.sendToDPID(4,msg)
         
             msg = of.ofp_flow_mod()
             msg.match = rmatch
             msg.actions.append(of.ofp_action_output(port = 1))
             core.openflow.sendToDPID(1,msg)
         
           if name_option == 'mp_join_opt':
             print name_option
             hash_key = beUnpack(option.rtoken)
             # Hash table will disjoint two-mp_join 
             Hash_table = dict()
             lista = list()
             lista.append([1,2,3])
             topologia = str(lista)   
             #Hash_table[hash_key] = topologia # Append token and topology
	     resultado = self.Hash_table.get(hash_key)

             if resultado is None:
               print "Nao tem Token, alocando em uma rota e inserindo na tabela..."
               match = of.ofp_match()
               match.nw_proto=6
               match.dl_type=0x800
               match.nw_src = packet_ipv4.srcip
               match.nw_dst = packet_ipv4.dstip
               match.tp_src = packet_tcp.srcport
               match.tp_dst = packet_tcp.dstport
                    
               # Reverse Match 
           
               rmatch = of.ofp_match()
               rmatch.nw_proto=6
               rmatch.dl_type=0x800
               rmatch.nw_src = packet_ipv4.dstip
               rmatch.nw_dst = packet_ipv4.srcip
               rmatch.tp_src = packet_tcp.dstport
               rmatch.tp_dst = packet_tcp.srcport
 
               # Path         
                           
               msg = of.ofp_flow_mod()
               msg.match = match
               msg.actions.append(of.ofp_action_output(port = 3))
               core.openflow.sendToDPID(1,msg)
                    
               msg = of.ofp_flow_mod()
               msg.match = match
               msg.actions.append(of.ofp_action_output(port = 2))
               core.openflow.sendToDPID(2,msg)

               msg = of.ofp_flow_mod()
               msg.match = match
               msg.actions.append(of.ofp_action_output(port = 2))
               core.openflow.sendToDPID(4,msg)
                  

               # Reverse Path 
               msg = of.ofp_flow_mod()
               msg.match = rmatch
               msg.actions.append(of.ofp_action_output(port = 3))
               core.openflow.sendToDPID(4,msg)
                    
	       msg = of.ofp_flow_mod()
               msg.match = match
               msg.actions.append(of.ofp_action_output(port = 1))
               core.openflow.sendToDPID(2,msg)

               msg = of.ofp_flow_mod()
               msg.match = rmatch
               msg.actions.append(of.ofp_action_output(port = 1))
               core.openflow.sendToDPID(1,msg)
               
              
               # adiciona o token:
               self.Hash_table[hash_key] = topologia
               
             else:
               print "Existe um valor dentro da tabela hash:", self.Hash_table

	   #else:
"""   	   #  return

def launch():

  from samples.pretty_log import launch
  launch()

  from openflow.spanning_tree import launch
  launch()

  from host_tracker import launch
  launch()

  from openflow.of_01 import launch
  launch(port= 1233)

  from openflow.discovery import launch
  launch()

  from misc.full_payload import launch
  launch()
		
  core.registerNew(Multiflow)
