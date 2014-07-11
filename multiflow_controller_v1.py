""" 
Marcus Sandri
Universidade Federal de Sao Carlos (UFSCar)
Federal University of Sao Carlos


This code it is used to link disjoint. 
In special, this branch is used to disjoint 
MP_CAPABLE and MP_JOIN.  

v. Beta 1.0

"""
from pox.core import core
import pox
import pox.lib.packet as pkt
from pox.lib.revent import *
from pox.openflow.discovery import Discovery
from pox.host_tracker import host_tracker
import pox.openflow.libopenflow_01 as of
from collections import *


class Auxiliar(object):
  """ """

  def __init__ (self):
    self.test = None
	
  def delete_value(self, input):
    """Delete repeated values 
    """

    output = []
    for x in input:
      if x not in output:
        output.append(x)
    return output


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
    
    auxiliar = Auxiliar()

    """ Used when switch-list assembling """
    
    for i in self.switch_memo:
      self.v.append(i[0])
    self.vertex = auxiliar.delete_value(self.v)
  
    for i in self.switch_memo:
      self.a.append((i[0], i[2]))
    self.edge = auxiliar.delete_value(self.a) 

  def _handle_HostEvent (self, event):
    """ Used to show Avalaible Hosts and its port numbers"""
    self.host_alive.append(event.entry) 
    print type(event.entry).__name__

  def _handle_PacketIn(self, event):
     packet = event.parsed
     packet_ipv4 = packet.find('ipv4')
     packet_tcp = packet.find('tcp')

     if packet.ARP_TYPE:
       """ If ARP, forwarding with L2/L3 if avaliable... """
       msg = of.ofp_flow_mod()
       msg.match = of.ofp_match.from_packet(packet)
       msg.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
       event.connection.send(msg)
     
     if not packet_tcp: return
     for option in packet_tcp.options:
       if isinstance(option, pkt.TCP.mptcp_opt):
         name_option = type(option).__name__ #,vars(option)
         if name_option == 'mp_join_opt':
           """ The 'IF' flow-control is used When there's a MP_JOIN
             packet """

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
           msg.actions.append(of.ofp_action_output(port = 2))
           core.openflow.sendToDPID(1,msg)
                    
           msg = of.ofp_flow_mod()
           msg.match = match
           msg.actions.append(of.ofp_action_output(port = 2))
           core.openflow.sendToDPID(2,msg)

           msg = of.ofp_flow_mod()
           msg.match = match
           msg.actions.append(of.ofp_action_output(port = 3))
           core.openflow.sendToDPID(4,msg)
                  

           # Reverse Path 
           msg = of.ofp_flow_mod()
           msg.match = rmatch
           msg.actions.append(of.ofp_action_output(port = 1))
           core.openflow.sendToDPID(4,msg)
                    
           msg = of.ofp_flow_mod()
           msg.match = rmatch
           msg.actions.append(of.ofp_action_output(port = 1))
           core.openflow.sendToDPID(2,msg)

           msg = of.ofp_flow_mod()
           msg.match = rmatch
           msg.actions.append(of.ofp_action_output(port = 1))
           core.openflow.sendToDPID(1,msg)

         else:
           return
   

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
		
  core.registerNew(Multiflow)
