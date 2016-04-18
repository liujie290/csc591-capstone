#read the data from the file into an RDD. convert to dict
from operator import *
import random
from pyspark.mllib.recommendation import *
import re
from functools import partial
from pyspark import SparkConf, SparkContext

sc=SparkContext()
#input data has u,v,distance
#input_data = sc.textFile("house_data.txt").map(graphparser).map(lambda x:(x[0],x[1],x[2]))

print "loading graph data from file"
# distnace local is 2d array holding (end_node, distance) for all pairs of nodes
distance_local=[]
f=open("house_data.txt",'r')
vertex_count=int(f.readline())
for i in range(vertex_count):
  distance_local.append([])
  for j in range(vertex_count):
      distance_local[i].append((j,0))
for line in f:
  splitted=line.split()
  distance_local[int(splitted[0])][int(splitted[1])]=(int(splitted[1]),float(splitted[2]))
  distance_local[int(splitted[1])][int(splitted[0])]=(int(splitted[0]),float(splitted[2]))

print "broadcasting distances for all workers"
# need to export our entire distance matrix...as we'll need it on the workers when we're calculating
# the new distances
distance=sc.broadcast(distance_local)

#randomly choose two medians. map each node to the element it's closest to
#medioids is just a list of vertices
local_medioids=random.sample(range(vertex_count),2)

print "Choosing initial medioids",local_medioids
while True:
#create a list of all vertices in the graph.
    vertices=sc.parallelize(range(vertex_count))
#broadcast our list of medioids. needed for finding the closest
#one in parallel
    medioids=sc.broadcast(local_medioids)


# returns the tuple of group index and vertex that was grouped
# We could parallelize this part maybe...but that would require
# a reduce function inside a map function...and I have no
# idea how you would even do that....maybe create
# the tuples first and then reduce by key? oh well...this
# is linear in K, so who cares...k is small
    def closest(vertex):
      index=-1
      min=100
      for i in range(len(medioids)):
          if (distance[vertex][medioids[i]] < min):
            index = i
            min=distance[vertex][medioids[i]]
      return (i, vertex)

#groups returns an RDD that's a list of (group,vertex) tuples
    groups=vertices.map(closest)

#this grabs a mapping of group to all vertices in the group (which we'll need in the next step)
#and then broadcasts it to everyone in the group
    group_list=groups.groupByKey().mapValues(list).broadcast()

#this function takes an element (group,vertex), and returns the sum of squares of from this node to
#every other element in the group
#returns a set (group, vertex, value)
    def calc_coherence(element):
      summ=0
      for i in group_list[element[0]][1]:
        summ+=distance_local[element[1]][i]**2
      return (element[0],(element[1],summ))

#for each group, create its own RDD, map it to the cluster metric for each element, then reduce it to find the minimum
#first map: take each vertex and it's assigned group...calculate the metric if it were the center of the group
#reduceby key: wil find the entry that produces the most tightly knit group
#map: converts the entry to a simple list of medioids
    new_medioids =groups.map(calc_coherence).reduceByKey(lambda a,b:a if a[1][1] < b[1][1] else b).map(lambda x:x[1][0]).collect()

    new_medioids.sort()
    same=True
    for i in len(new_medioids):
      if medioids[i] != new_medioids[i]:
          same = False
          break
    if same:
       f=open("graph.clusters", 'w')
       f.write(group_list.collect())
       break


#if we didn't break out of the while loop, set the new medioids, and go to town again!
    mediods = new_mediods
