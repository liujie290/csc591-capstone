import download_data as dd
import matplotlib.pyplot as plt
import igraph

if __name__ == "__main__":
  

  sen_modularities = [];
  sen_clusters = [];

  # 101 takes us back to 1990
  for x in range(101,114):
      
      data = dd.senatedata(x)
      graph = dd.makegraph(data)

      # fast greedy tended to be the most reasonable cluster
      community = graph.community_fastgreedy().as_clustering()
      filename = "senate" + str(x) + ".png"
      igraph.plot(community, filename)
      
      # keep track of cluster size and modularity
      sen_clusters.append(community.__len__())
      sen_modularities.append(community.modularity)
      
  print sen_clusters
  print "average senate cluster size is " + str(sum(sen_clusters) / float(len(sen_clusters)))
  print sen_modularities
  print "average senate modularity is " + str(sum(sen_modularities) / float(len(sen_modularities)))

  house_modularities = [];
  house_clusters = [];

  # 101 takes us back to 1990
  for x in range(101,114):
      
      data = dd.housedata(x)
      graph = dd.makegraph(data)

      # fast greedy tended to be the most reasonable cluster
      community = graph.community_fastgreedy().as_clustering()
      filename = "house" + str(x) + ".png"
      igraph.plot(community, filename)
      
      # keep track of cluster size and modularity
      house_clusters.append(community.__len__())
      house_modularities.append(community.modularity)
      
  # cluster size tends to be 2 ... matching two predominant parties
  print house_clusters
  print "average house cluster size is " + str(sum(house_clusters) / float(len(house_clusters)))
  print house_modularities
  print "average house modularity is " + str(sum(house_modularities) / float(len(house_modularities)))

   
