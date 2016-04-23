#!/usr/bin/python
from download_data import *
import pickle 
import collections

graphdata = 'allsenates.pydata'
loadgraph = False # If true, will load the graph. Else, will make and save the
                  # graph before continuing.

if loadgraph:
  print "Loading graph."
  senategraph = igraph.Graph()
  senategraph = senategraph.Read_Pickle(graphdata)
else:
  with open('congress.pydata', 'rb') as data:
    allhouses  = pickle.load(data)
    allsenates = pickle.load(data)
  print "Making graph."
  senategraph = makegraph(allsenates)
  del(allhouses, allsenates)
  # Define some attributes from info, since we need to delete the info attribute
  # to be able to save.
  # collections.Counter(list).most_common(1) returns the most common item as
  #    [(item, count)].
  partymode = [int(collections.Counter(info.party).most_common(1)[0][0])
               for info in senategraph.vs["info"]]
  senategraph.vs["party"] = partymode
  # Mean congress will be used to create the drawing order.
  congresses = [[int(congressnum) for congressnum in list(info.congresses)] 
                for info in senategraph.vs["info"]]
  meancongress = [sum(congress)/float(len(congress)) for congress in congresses]
  senategraph.vs["name"] = [list(info.name)[0] for info 
                                               in senategraph.vs["info"]]
  # Initialize static node attributes that will control graphing.
  senategraph.vs["order"] = meancongress
  # We need to remove the info attribute to save the graph.
  del senategraph.vs["info"]
  print "Saving graph."
  senategraph.write_pickle(graphdata)

# Initialize the node colors.
def initnodecolor(partycode):
  if partycode == 100:
    # Democrat
    return "blue"
  elif partycode == 200:
    # Republican
    return "red"
  elif partycode == 29:
    # Whig, became Republicans
    return "firebrick"
  elif partycode == 1:
    # Federalists
    return "fuchsia"
  elif partycode == 555:
    # Jackson party
    return "purple"
  elif partycode == 1275:
    # Anti-Jackson party, from democratic-republicans, became whigs.
    return "yellow"
  elif partycode == 5000:
    # Pro-administration party
    return "coral"
  elif partycode == 4000:
    # Anti-administration party: Madison+Jefferson, anti-federalists.
    return "aqua"
  elif partycode == 22:
    # Adams party, also anti-jackson
    return "khaki"
  else:
    return "green"

edge_width = 2
vertex_size = 30

def initgraph(graph):
  graph.vs["color"] = [initnodecolor(partycode) for partycode 
                                                in graph.vs["party"]] 
  graph.vs["shape"] = "circle"
  graph.vs["size"] = vertex_size
  graph.es["color"] = "black"
  graph.es["width"] = edge_width
  graph.es["lty"] = 1
  numedges = [len(graph.incident(vertexnum))
                  for vertexnum
                  in range(graph.vcount())]
  graph.vs["numedges"] = numedges

def minweightify(graph, minweight):
  # White out edges that don't make the cut.
  edgeweights = graph.es["weight"]
  for edgeid, weight in enumerate(edgeweights):
    if weight <= minweight:
      graph.es[edgeid]["color"] = "white"
      graph.es[edgeid]["width"] = 0
      graph.es[edgeid]["lty"] = 0
      vertexnum = graph.es[edgeid].tuple
      graph.vs[vertexnum[0]]["numedges"] -= 1
      graph.vs[vertexnum[1]]["numedges"] -= 1
  # White out vertices that no longer have a positive number of edges.
  #colors = ["white" if numedges == 0 else graph.vs[vid]["color"]
  #          for vid, numedges in enumerate(graph.vs["numedges"])]
  #graph.vs["color"] = colors
  shapes = ["none" if numedges == 0 else "circle"
            for vid, numedges in enumerate(graph.vs["numedges"])]
  graph.vs["shape"] = shapes
  
def makeplot(graph, minweight, graphlayout, filename='plots/senate_{}.png'):
  outfile = filename.format(str(int(100*minweight)).zfill(3))
  initgraph(graph)
  minweightify(graph, minweight)
  igraph.plot(graph, outfile, bbox=(0,0,10000,10000), layout=graphlayout)

# Remove nodes that never voted (possibly presidents, people who died before
# having the chance to vote, etc).
initgraph(senategraph)
nevervoted = [vertexid for vertexid,numedges 
                       in enumerate(senategraph.vs["numedges"]) 
                       if numedges == 0]
senategraph.delete_vertices(nevervoted)
# Calculate the layout once so nodes don't change position.
layout = senategraph.layout("fr")
for w in [num/100.0 for num in range(101)]:
  print str(w),"= Voting Together Percentage", str(int(100*(1+w)/2))
  makeplot(senategraph, w, graphlayout=layout)


