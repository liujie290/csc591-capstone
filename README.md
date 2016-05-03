# csc591-capstone
cluster.py:

pyspark application to calculate the K medioids clustering of a graph
<p>pyspark cluster.py &lt;input&gt; &lt;output&gt; &lt;K&gt; (&lt;iterations&gt;)<p>
input: the input graph of the form
&lt;vertex_count&gt;
&lt;i&gt; &lt;name&gt;
&lt;u&gt; &lt;v&gt; &lt;d&gt;
...

the first &lt;vertex_count&gt; lines contain a vertex index and the associated name
the remaining lines contain edges...with an edge of weight &lt;d&gt; between &lt;u&gt; and &lt;v&gt;
unlisted edges are assumed to be infinite. All edges are bidirectional

output: if an iteration count is not provided, we output the clusters
&lt;medioid&gt;: &lt;member_1&gt; &lt;member_2&gt;...

if an iteration count IS provided, we provide a histogram of how many times a congressman was a medioid. Only those with non-zero values are listed.
&lt;medioid&gt;: &lt;count&gt;

K: the number of clusters

download_data.py
downloads congress vote data
python download_data.py (house|senate) &lt;start&gt; &lt;end&gt; &lt;output&gt;

specify which house you want to download, the range of sessions you wish to include (inclusive), as well as the output file. Output is of the form above intended to be slurped by clusters.py
