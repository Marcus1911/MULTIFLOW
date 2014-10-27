from pox.core import core
import pox.lib.packet as pkt
import pox.lib.pxpcap.parser as pxparse
import networkx as nx
import time

startTime = time.time()
G=nx.path_graph(100)


counter = 0
def beUnpack(byte):
       """ Converts byte string to integer. Use Big-endian byte order."""
       try:
         return sum([ord(b) << (8 * i) for i, b in enumerate(byte[::-1])])
       except:
         return 'impossible to convert'

def Multiflow (data, parser):

  global counter
  counter += 1
  packet = pkt.ethernet(data)
  packet_tcp = packet.find('tcp')
  if not packet_tcp: return
  if packet_tcp.SYN and packet_tcp.ACK: return
  if packet_tcp.SYN is True:
   
    for option in packet_tcp.options:
      if isinstance(option, pkt.TCP.mptcp_opt):
        name_option = type(option).__name__ #,vars(option)
        if name_option == 'mp_capable_opt':
          print "MP_CAPABLE\n"
        if name_option == 'mp_join_opt':
          hash_key = beUnpack(option.rtoken)
          Hash_table = dict()
          lista = list()
          path = nx.single_source_shortest_path(G,0)
          lista.append([1,2,3])
          topologia = str(lista)  
          Hash_table[hash_key] = topologia # Append token and topology 
	  resultado = Hash_table.get(hash_key)
          print "MP_JOIN", hash_key
         
          if resultado is None:
           # print "There's no Token. Multiflow will add for you..."
            path = nx.single_source_shortest_path(G,0)
            Hash_table[hash_key] = topologia

          else:
               #print "Path:", Hash_table[hash_key] 
               path = nx.single_source_shortest_path(G,0)
                                    
  return
  elapsedTime = time.time() - startTime
  print elapsedTime
def launch (filename):
  data = open(filename, "r").read()
  p = pxparse.PCapParser(callback=Multiflow)
  p.feed(data)
  core.quit()



