""" 

Marcus Sandri
Universidade Federal de Sao Carlos

v. Beta 1.0

"""
from pox.core import core
import pox
import pox.lib.packet as pkt
from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
from pox.openflow.discovery import Discovery
from pox.host_tracker import host_tracker
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr
import matplotlib.pyplot as plt
from collections import *
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import itertools
import hashlib as hash

#log = core.getLogger()

class Happy_Blue(EventMixin):
  def __init__ (self):
    self.connection = None
    self.ports = None
    self.dpid = None
    self.timer = None
    self.rkeys = []
    self.switch_memo = []
    self.host_alive = []
    self.rkey = []
    self.v = []
    self.a = []

    def startup ():
      core.openflow.addListeners(self, priority=0)
      core.openflow_discovery.addListeners(self)
      core.host_tracker.addListeners(self)
    core.call_when_ready(startup, ('openflow','openflow_discovery', 'host_tracker'))

  def _handle_LinkEvent (self, event):
    # Captura eventos dos comutadores.
    l = event.link
    self.switch_memo.append([l.dpid1,l.port1,l.dpid2,l.port2])

  def _handle_HostEvent (self, event):
    # captura evento dos hospedeiros.
    self.host_alive.append(event.entry)  # MAC Entry

  def _handle_PacketIn(self, event):
     packet = event.parsed
     packet_ipv4 = packet.find('ipv4')
     packet_udp = packet.find('udp')
     packet_tcp = packet.find('tcp')
     #print "porta antes: \n", packet_tcp.srcport



     if packet.ARP_TYPE:
       msg = of.ofp_flow_mod()
       msg.match = of.ofp_match.from_packet(packet)
       msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
       event.connection.send(msg)

     if packet_tcp:
       if packet_tcp.SYN:

         def beUnpack(byte):
           return sum([ord(b) << (8 * i) for i, b in enumerate(byte[::-1])])

         try:
           for option in packet_tcp.options:
             if isinstance(option, pkt.mp_capable_opt):
               keys = beUnpack(option.skey)
             
               print "key:", packet_tcp.srcport, packet_tcp.dstport, packet_ipv4.srcip, option.skey
 # MATCH
               match = of.ofp_match()
               match.nw_proto=6
               match.dl_type=0x800
               match.nw_src = packet_ipv4.srcip
               match.nw_dst = packet_ipv4.dstip
               match.tp_src = packet_tcp.srcport
               match.tp_dst = packet_tcp.dstport
                    
                  # MATCH REVERSO
               rmatch = of.ofp_match()
               rmatch.nw_proto=6
               rmatch.dl_type=0x800
               rmatch.nw_src = packet_ipv4.dstip
               rmatch.nw_dst = packet_ipv4.srcip
               rmatch.tp_src = packet_tcp.dstport
               rmatch.tp_dst = packet_tcp.srcport
 
                  # REGRA (ACTION)
                  
                    
                  # Regra Destino
               msg = of.ofp_flow_mod()
               msg.match = match
               msg.actions.append(of.ofp_action_output(port = 2))
               core.openflow.sendToDPID(1,msg)
                    
               msg = of.ofp_flow_mod()
               msg.match = match
               msg.actions.append(of.ofp_action_output(port = 2))
               core.openflow.sendToDPID(2,msg)
                  

                  # Destino Invertido 
               msg = of.ofp_flow_mod()
               msg.match = rmatch
               msg.actions.append(of.ofp_action_output(port = 1))
               core.openflow.sendToDPID(2,msg)
                    
               msg = of.ofp_flow_mod()
               msg.match = rmatch
               msg.actions.append(of.ofp_action_output(port = 1))
               core.openflow.sendToDPID(1,msg)

         except:
           print "Exception \n"
   

def launch():

  from samples.pretty_log import launch
  launch()

  from openflow.spanning_tree import launch
  launch()

  from host_tracker import launch
  launch()

  from openflow.of_01 import launch
  launch(port= 1234)

  from openflow.discovery import launch
  launch()

  from misc.full_payload import launch
  launch()
		
  core.registerNew(Happy_Blue)
