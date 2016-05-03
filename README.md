# csc591-capstone
cluster.py:

pyspark application to calculate the K medioids clustering of a graph
pyspark cluster.py <input> <output> <K> (<iterations>)
input: the input graph. of the form
&ltvertex_count&gt
&lti&lt <name&lt
<u> <v> <d>
...

the first <vertex_count> lines contain a vertex index and the associated name
the remaining lines contain edges...with an edge of weight <d> between <u> and <v>
unlisted edges are assumed to be infinite. All edges are bidirectional

output: if an iteration count is not provided, we output the clusters
<medioid>: <member_1> <member_2>...

if an iteration count IS provided, we provide a histogram of how many times a congressman was a medioid. Only those with non-zero values are listed.
<medioid>: <count>

K: the number of clusters

download_data.py
downloads congress vote data
python download_data.py (house|senate) <start> <end> <output>

specify which house you want to download, the range of sessions you wish to include (inclusive), as well as the output file. Output is of the form above intended to be slurped by clusters.py
