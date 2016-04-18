#read the data from the file into an RDD. convert to dict
from operator import *
import random
from pyspark.mllib.recommendation import *
import re

#input data has u,v,distance
#input_data = sc.textFile("house_data.txt").map(graphparser).map(lambda x:(x[0],x[1],x[2]))

# distnace local is 2d array holding (end_node, distance) for all pairs of nodes
distance_local=[]
with "house_data.txt" as f:
  vertex_count=(int)f.readline().split()
  for i in range(vertex_count):
      distance_local.append([])
      for j in range(vertex_count):
      distance_local[i].append((0,0))
  for line in f:
      splitted=line.split()
      distance_local[int(splitted[0])][int(splitted[1])]=(int(splitted[1]),float(splitted[2]))
      distance_local[int(splitted[1])][int(splitted[0])]=(int(splitted[0]),float(splitted[2]))

#distance_rdd holds one RDD for the distnace vector emanating at a given node
#it gets initialized to the distances in the graph
distance_rdd=[]
for i in range(vertex_count):
    distance_rdd.append(sc.parallelize(distance_local[i]))

'''
def new_best(point):
  if point[0] > distance_local[i][j] + distance_local[j][point[1]]:
      return (distance_local[i][j] + distance_local[j][point[1]], point[1]);
  else
      return point


for j in range(len(distance_local)):
  for i in range(len(distance_local)):
    if i == j continue;
#broadcast the new distances
    d_ij=distance_rdd[i].collect()[j][0]
    distnce_rdd[i]=distance_rdd[i].map(new_best)


'''
  
#randomly choose two medians. map each node to the element it's closest to
mediods=random.sample(vertex_count,2)
vertices=scc.parallelize(range(vertex_count))

# returns the tuple of group index and vertex that was grouped
def closest(vertex):
  int index
  int min=100
  for i range len(mediods):
      if (distance_local[vertex][mediods[i]] < min):
        index = i
        min=distance_local[vertex][mediods[i]]
  return (i, vertex)

#groups returs an RDD that's a list of (group,vertex)tuples
groups=vertices.map(closest)
#this grabs a mapping of group to all vertices in the group (which we'll need in the next step
local_groups=groups.groupByKey().mapValues(list).collect()
'''
groups={}
for i in mediods:
    groups[i]=[]
local_mapping=mapping.collect()
#groups is a dict mapping a mediod to a list of the members of its group
#we take the mappings that the previous map provided and add the vertices to the appropriate group
for i in len(local_mapping):
    groups[local_mapping[i]].append(i)

# we parallelize our groups now, and for each one, calculate the minimum mediod
groups_rdd = sc.parallelize(groups)
'''

#this function takes an element (group,vertex), and returns the sum of squares of from this node to
#every other element in the group
def calc_coherence(element):
  summ=0
  for i in local_groups[element[0]]:
    summ+=distance_local[element[1]][i]

#for each group, create its own RDD, map it to the cluster metric for each element, then reduce it to find the minimum
group_rdds=[]
for i in local_groups:
    sc.parallelize(i).flatMapmap(calc_coherence)

#changes each group into a list of 
best_distances=groups.map(distance_per_element)
for i in 

#group nodes by key
#create reduce which calculates cost metric of group with a given mediod
#reduce on min selection of new median
#repeat until convergeance

#collect groupings, output to file
#compare against selected party data
