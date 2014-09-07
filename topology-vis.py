import json
import networkx as nx
import matplotlib.pyplot as plt
import urllib2
import sys, getopt

try:
  opts, args = getopt.getopt(sys.argv[1:],"u:f:",["url=","file="])
except getopt.GetoptError:
  print 'topo.py -u <url> or topo.py -f <file>'
  sys.exit(2)

url = None 
inputfile = ""
for opt, arg in opts:
  if opt == '-u':
    url = arg
  elif opt == '-f':
    inputfile = arg
## Load data from json
api="/api/v1/topology/"
summary_api="summary"

topologies=""
##Get list of topologies
if url is not None:
  rest_url = url + api + summary_api
  topologies=json.load(urllib2.urlopen(rest_url))['topologies']
else:
  topologies=json_load(open(inputfile))

topo_id=[]
for topology in topologies:
  topo_id.append(topology['id'])

##Get details of topology
visualization_api="/visualization"
for id in topo_id:
  rest_url = url + api + id + visualization_api
  json_data=json.load(urllib2.urlopen(rest_url))
  labels={}

  ## initialize a directed graph
  G = nx.DiGraph()
  edge_labels=dict()
  nodelist=[]
  for key in json_data.keys():
    ## filter acker and system nodes
    if key =='__acker' or key =='__system':
      continue
    storm_component=json_data[key]
    inputs=storm_component[':inputs'] 
    G.add_node(key)
    labels[key]=key
    nodelist.append(key)
    for input in inputs:
      node=input[':component']
      ##Filter edges having acker and system nodes
      if node =='__acker' or node =='__system':
        continue
      stream = input[':stream']
      edge_labels[(key, input[':component'])] = stream 
      G.add_edge(input[':component'], key)

  pos = nx.circular_layout(G, dim=2, scale=2)

  number_of_nodes= len(G.nodes())
  for edge in G.edges():
    node=edge[0]
    try:
      ind=nodelist.index(node)
      del nodelist[ind]
    except:
      pass

  spout=nodelist[0]

  ##Create graph
  nx.draw(G, pos=pos)
  ##Add node labels
  nx.draw_networkx_labels(G, pos,labels, font_size=15)
  ##Add edge labels
  nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
  ##Change edge color
  nx.draw_networkx_edges(G,pos=pos, edge_color='b')

  ##show graph
  plt.show()
