#read the data from the file into an RDD. convert to dict
from operator import *
import random
from pyspark.mllib.recommendation import *
import re
from functools import partial
from pyspark import SparkConf, SparkContext
import sys

sc=SparkContext()
#input data has u,v,distance
#input_data = sc.textFile("house_data.txt").map(graphparser).map(lambda x:(x[0],x[1],x[2]))

print "loading graph data from file"
# distnace local is 2d array holding (end_node, distance) for all pairs of nodes
distance_local=[]
f=open(sys.argv[1],'r')
vertex_count=int(f.readline())
names={}
for i in range(vertex_count):
    name_line=f.readline().split()
    names[int(name_line[0])]=name_line[1]
for i in range(vertex_count):
  distance_local.append([])
  for j in range(vertex_count):
      distance_local[i].append(sys.float_info.max / 100)
      if i == j:
          distance_local[i][j] = 0
for line in f:
  splitted=line.split()
  distance_local[int(splitted[0])][int(splitted[1])]=float(splitted[2])
  distance_local[int(splitted[1])][int(splitted[0])]=float(splitted[2])

# we keep a histogram of how often a given entry arises
histo={}
iterations=0

print "broadcasting distances for all workers"
# need to export our entire distance matrix...as we'll need it on the workers when we're calculating
# the new distances
distance=sc.broadcast(distance_local)

for i in range(int(sys.argv[4]) if len(sys.argv)==5 else 1):
#randomly choose two medians. map each node to the element it's closest to
#medioids is just a list of vertices
    local_medioids=random.sample(range(vertex_count),int(sys.argv[3]))
    local_medioids.sort()

    print "Choosing initial medioids",local_medioids
    while True:
#create a list of all vertices in the graph.
        vertices=sc.parallelize(range(vertex_count))
#broadcast our list of medioids. needed for finding the closest
#one in parallel
        medioids=sc.broadcast(local_medioids)

        print "mapping all vertices to closest medioid"
# returns the tuple of group index and vertex that was grouped
# We could parallelize this part maybe...but that would require
# a reduce function inside a map function...and I have no
# idea how you would even do that....maybe create
# the tuples first and then reduce by key? oh well...this
# is linear in K, so who cares...k is small
        def closest(vertex):
          index=-1
          minn=100
          for i in range(len(medioids.value)):
              if (distance.value[vertex][medioids.value[i]] < minn):
                index = i
                minn=distance.value[vertex][medioids.value[i]]
          return (medioids.value[index], vertex)

#groups returns an RDD that's a list of (group,vertex) tuples
        groups=vertices.map(closest)

#this grabs a mapping of group to all vertices in the group (which we'll need in the next step)
#and then broadcasts it to everyone in the group
        group_list=groups.groupByKey().mapValues(list)
        group_list_local=group_list.collect()
        group_dict={}
        for i in group_list_local:
            group_dict[i[0]]=i[1]
        group_dict_b=sc.broadcast(group_dict)

#this function takes an element (group,vertex), and returns the sum of squares of from this node to
#every other element in the group
#returns a set (group, vertex, value)
        def calc_coherence(element):
          summ=0
          for i in group_dict_b.value[element[0]]:
            summ+=distance.value[element[1]][i]**2
          return (element[0],(element[1],summ))

        print "calculating new set of medioids"
#for each group, create its own RDD, map it to the cluster metric for each element, then reduce it to find the minimum
#first map: take each vertex and it's assigned group...calculate the metric if it were the center of the group
#reduceby key: wil find the entry that produces the most tightly knit group
#map: converts the entry to a simple list of medioids
        new_medioids = groups.map(calc_coherence).reduceByKey(lambda a,b:a if a[1] < b[1] else b).map(lambda x:x[1][0]).collect()

        new_medioids.sort()
        print "new medioids are",new_medioids

        same=True
        for i in range(len(new_medioids)):
          if local_medioids[i] != new_medioids[i]:
              same = False
              break
        if same:
           if len(sys.argv) == 5:
             for i in new_medioids:
                 if not i in histo.keys():
                     histo[i]=0
                 histo[i]+=1
             iterations += 1
             break
           else:
               f=open(sys.argv[2], 'w')
               for i in new_medioids:
                   f.write("%s:" %(names[i]))
                   for j in group_dict[i]:
                       f.write(" %s" %(names[j]))
                   f.write("\n")
               break


#if we didn't break out of the while loop, set the new medioids, and go to town again!
        local_medioids = new_medioids

if len(sys.argv) == 5:
    f=open(sys.argv[2], 'w')
    for i in histo.keys():
        f.write("%s: %d\n" %(names[i],histo[i]))

