#!/usr/bin/python
import download_data as data
import igraph
import sys
import matplotlib.pyplot as plt

# Comparison.py   

# stores graph data dowloaded from download_data module
input_data = None

# stores the modularity scores obtained by the different algorithms
# (Walktrap, Leading Eigenvector, and FastGreedy)
walk_mods = []
eigen_mods = []
fast_mods = []

# stores the number of communities obtained by the different algorithms
# (Walktrap, Leading Eigenvector, and FastGreedy)
walk_comms = []
eigen_comms = []
fast_comms = []

def main():
  if (len(sys.argv) != 4):
    print "usage: comparison.py senate|house starting_roll_call ending_roll_call"
  
  # indicates whether we're analyzing house or senate data
  branch = sys.argv[1]
  
  # stores starting and ending session prefix
  session1 = int(sys.argv[2])
  session2 = int(sys.argv[3])
  
  # runs the Walktrap, Leading Vector, FastGreedy algorithms on the input data
  # iterates through each graph in the given range
  for i in range(session1, session2 + 1):
      if (branch == "senate"):
          input_data = data.senatedata(i)      
      elif (branch == "house"):
          input_data = data.housedata(i)
        
      # this is the input graph
      graph = data.makegraph(input_data)
    
      # runs each algorithm on the input graph
      result_walk = graph.community_walktrap(weights = None, steps = 4).as_clustering()    
      result_eigen = graph.community_leading_eigenvector(clusters = None, weights = None, arpack_options = None)    
      result_fast = graph.community_fastgreedy(weights = None).as_clustering()      
      
      #some other algorithms I was considering running
      #result = graph.community_edge_betweenness(clusters = None, directed = False, weights = "weight").as_clustering()
      #result = graph.community_infomap(edge_weights = "weight", vertex_weights = None, trials = 10)
      #result = graph.community_multilevel(weights = "weight", return_levels = False)
      #result = graph.community_label_propagation(weights = "weight", initial = None, fixed = None)
  
      # plots and saves the resulting clustering in a .png file
      igraph.plot(result_walk, "walk_" + branch + "_sess" + str(i) + ".png")
      igraph.plot(result_eigen, "eigen_" + branch + "_sess" + str(i) + ".png")
      # already have these graphs  
      # igraph.plot(result_fast, "fast_" + branch + "_sess" + str(i) + ".png")  
      
      # stores the resulting # of communities produced by each algorithm
      walk_comms.append(result_walk.__len__())
      eigen_comms.append(result_eigen.__len__())
      fast_comms.append(result_fast.__len__())
      
      # stores the resulting modularity score produced by each algorithm
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
  
  # plots the modularity scores
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
