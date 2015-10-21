from pox.core import core
import pox.lib.packet as pkt
import pox.lib.pxpcap.parser as pxparse
import networkx as nx
import time

G=nx.path_graph(100)

log = core.getLogger()

counter = 0
def beUnpack(byte):
       """ Converts byte string to integer. Use Big-endian byte order."""
       try:
         return sum([ord(b) << (8 * i) for i, b in enumerate(byte[::-1])])
       except:
         return 'impossible to convert'

def Multiflow (data, parser):
    
  packet = pkt.ethernet(data)
  packet_tcp = packet.find('tcp')

  if not packet_tcp: return
  if packet_tcp.SYN and packet_tcp.ACK: return
  if packet_tcp.SYN is True:
   
    for option in packet_tcp.options:
      if isinstance(option, pkt.TCP.mptcp_opt):
        name_option = type(option).__name__ #,vars(option)
        if name_option == 'mp_capable_opt':
            #changed to log.info()  
          log.info("MP_CAPABLE\n")           
        if name_option == 'mp_join_opt':
          hash_key = beUnpack(option.rtoken)
          Hash_table = dict()
          lista = list()
          path = nx.single_source_shortest_path(G,0)
          lista.append([1,2,3])
          topologia = str(lista)  
          #Hash_table[hash_key] = topologia # Append token and topology 
          #FIXME: Associate the hash in the constructor

	  resultado = Hash_table.get(hash_key)
          #keeped with print, due log.info errors
          print "MP_JOIN", resultado 
         
          if resultado is None:  
            #Hash_table[hash_key] = topologia
            log.info("Matrix is empty. Populating...")
            #...Gives the shortest-path in the topology  
            path = nx.single_source_shortest_path(G,0)
            
            #Add pruned topology and associate it with the token 
            Hash_table[hash_key] = topologia
           
            

          else:
              
               try:
                 print "There's a token"
                 NewTopology = Hash_table.get(hash_key)
                 #.. Gives the shortest-path in the topology
                 path = nx.single_source_shortest_path(G,0)

                 #Add pruned topology and associate it with the token
                 Hash_table[hash_key] = NewTopology

               except:
                 #TODO: TEST IT! 

                 print "There's no more shortest-paths"

                 # OF rules for dropping


                                    
  return


def launch (filename):
  data = open(filename, "r").read()
  p = pxparse.PCapParser(callback=Multiflow)
  p.feed(data)
  core.quit()



