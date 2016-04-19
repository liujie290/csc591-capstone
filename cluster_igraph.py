import download_data as dd
import matplotlib.pyplot as plt
import igraph
import numpy

# Usage: python cluster_igraph.py (no params)
# This module gathers all house and senate data from th 101st to 113th
# and calculates clusters from each of them individually. It plots each
# and compares differences between house and senate
if __name__ == "__main__":

  # get all roll calls from 101st through 113th
  roll_range = range(101,114)

  sen_modularities = [];
  sen_clusters = [];

  # for senates 101 - 113
  for x in roll_range:
      
      data = dd.senatedata(x)
      graph = dd.makegraph(data)

      # fast greedy tended to be the most reasonable cluster
      community = graph.community_fastgreedy().as_clustering()
      filename = "senate" + str(x) + ".png"
      igraph.plot(community, filename)
      
      # keep track of cluster size and modularity
      sen_clusters.append(community.__len__())
      sen_modularities.append(community.modularity)

  print "average number of senate clusters is " + str(sum(sen_clusters) / float(len(sen_clusters)))
  avg_sen_modularity = sum(sen_modularities) / float(len(sen_modularities))
  print "average senate modularity is " + str(avg_sen_modularity)

  house_modularities = [];
  house_clusters = [];

  # # for houses 101 - 113
  for x in roll_range:
      
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
  print "average number of house clusters is " + str(sum(house_clusters) / float(len(house_clusters)))
  avg_house_modularity = sum(house_modularities) / float(len(house_modularities))
  print "average house modularity is " + str(avg_house_modularity)

  # display plot to compare modularities
  plt.plot(roll_range, sen_modularities, 'bo', label="Senate")
  plt.plot(roll_range, house_modularities, 'yo', label="House")
  plt.ylabel('Modularity')
  plt.xlabel('House/Senate Roll Call')
  plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)

  # compute linear trend for senate and add to plot
  z = numpy.polyfit(roll_range, sen_modularities, 1)
  p = numpy.poly1d(z)
  plt.plot(roll_range,p(roll_range),'b--')

  # compute linear trend for house and add to plot
  z_2 = numpy.polyfit(roll_range, house_modularities, 1)
  p_2 = numpy.poly1d(z_2)
  plt.plot(roll_range,p_2(roll_range),'y--')

  # save plot
  plt.savefig("modularities.png", bbox_inches='tight')

  # clear plot for new one
  plt.clf()

  # create bar graph to show modularity comparison average
  width = 1/1.9
  x_axis = ["Senate", "House"]
  y_axis = [avg_sen_modularity, avg_house_modularity]
  barlist = plt.bar(range(len(x_axis)), y_axis, width, align='center')
  plt.xticks(range(len(x_axis)), x_axis, size='small')
  plt.ylabel('Modularity')
  plt.title('Average Modularity Since 101st Senate/House')

  # set colors the same asscatter plot
  barlist[0].set_color('b')
  barlist[1].set_color('y')

  # save bar graph
  plt.savefig("modularities_bar.png", bbox_inches='tight')


