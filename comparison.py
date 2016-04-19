#!/usr/bin/python
import download_data as data
import igraph
import sys
import matplotlib.pyplot as plt

input_data = None
walk_mods = []
eigen_mods = []
fast_mods = []

walk_comms = []
eigen_comms = []
fast_comms = []

def main():
  if (len(sys.argv) != 4):
    print "usage: comparison.py senate|house starting_roll_call ending_roll_call"
  branch = sys.argv[1]
  session1 = int(sys.argv[2])
  session2 = int(sys.argv[3])
  
  for i in range(session1, session2 + 1):
      if (branch == "senate"):
          input_data = data.senatedata(i)      
      elif (branch == "house"):
          input_data = data.housedata(i)
  
      graph = data.makegraph(input_data)
    
      result_walk = graph.community_walktrap(weights = "weight", steps = 4).as_clustering()    
      result_eigen = graph.community_leading_eigenvector(clusters = None, weights = "weight", arpack_options = None)    
      result_fast = graph.community_fastgreedy(weights = "weight").as_clustering()      
      
      #result = graph.community_edge_betweenness(clusters = None, directed = False, weights = "weight").as_clustering()
      #result = graph.community_infomap(edge_weights = "weight", vertex_weights = None, trials = 10)
      #result = graph.community_walktrap(weights = "weight", steps = 4).as_clustering() 
      #result = graph.community_edge_betweenness(clusters = None, directed = False, weights = "weight").as_clustering()
      #result = graph.community_multilevel(weights = "weight", return_levels = False)
      #result = graph.community_label_propagation(weights = "weight", initial = None, fixed = None)
  
      igraph.plot(result_walk, "walk_" + branch + "_sess" + str(i) + ".png")
      igraph.plot(result_eigen, "eigen_" + branch + "_sess" + str(i) + ".png")
      # already have these graphs  
      # igraph.plot(result_fast, "fast_" + branch + "_sess" + str(i) + ".png")  
      
      walk_comms.append(result_walk.__len__())
      eigen_comms.append(result_eigen.__len__())
      fast_comms.append(result_fast.__len__())
      
      walk_mods.append(result_walk.modularity)
      eigen_mods.append(result_eigen.modularity)
      fast_mods.append(result_fast.modularity)
  
  print "walk comms: "
  print walk_comms
  
  print "eigen comms: "
  print eigen_comms
  
  print "fast comms: "
  print fast_comms
  
  print "walk mods: "
  print walk_mods
  
  print "eigen mods: "
  print eigen_mods
  
  print "fast mods: "
  print fast_mods
  
  sessions = range(session1, session2 + 1)
  plt.plot(sessions, walk_mods)
  plt.plot(sessions, eigen_mods)
  plt.plot(sessions, fast_mods)
  plt.ylabel("Modularity")
  plt.xlabel("Senate Roll Call")
  plt.legend(["Leading Eigenvector Modularity", "Walktrap Modularity", "FastGreedy Modularity"], loc = "lower right")
  plt.show()
  
if __name__ == "__main__":
    main()   
