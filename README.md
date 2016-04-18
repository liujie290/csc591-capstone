# csc591-capstone
cluster.py:

pyspark application to calculate the K medioids clustering of a graph
pyspark cluster.py <input> <output> <K>
input: the input graph. of the form
<vertex_count>
<u> <v> <d>
...

unlisted edges are assumed to be infinite. All edges are bidirectional

output: the clusters
<medioid>: <member_1> <member_2>...

K: the number of clusters
