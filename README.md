# csc591-capstone

## Setup

Dependencies can be loaded from pip dependency file included called deps.txt.

Spark required.

leiningen from http://leiningen.org/

## Medioid Cluster
cluster.py:

pyspark application to calculate the K medioids clustering of a graph
```pyspark cluster.py input output K (iterations)```

input: the input graph of the form
```
vertex_count
i name
u v d
```

the first &lt;vertex_count&gt; lines contain a vertex index and the associated name
the remaining lines contain edges...with an edge of weight &lt;d&gt; between &lt;u&gt; and &lt;v&gt;
unlisted edges are assumed to be infinite. All edges are bidirectional

output: if an iteration count is not provided, we output the clusters
&lt;medioid&gt;: &lt;member_1&gt; &lt;member_2&gt;...

if an iteration count IS provided, we provide a histogram of how many times a congressman was a medioid. Only those with non-zero values are listed.<br>
&lt;medioid&gt;: &lt;count&gt;

K: the number of clusters

### Data file provided

Data file provided from:
```python download_data.py senate 100 113 senate_100_113.graph```

To run:
```pyspark cluster.py senate_100_113.graph <output> <K> <iterations>```

### To download new data
download_data.py<br>
downloads congress vote data<br>
python download_data.py (house|senate) &lt;start&gt; &lt;end&gt; &lt;output&gt;

specify which house you want to download, the range of sessions you wish to include (inclusive), as well as the output file. Output is of the form above intended to be slurped by clusters.py


## Scraper

### Description

To create a corpus of text, a clojure app was made to scrape the websites and download the data. This does not have to be run. A zip called datafile.zip has the corpus downloaded for the report. It is to be used with word2vec.ipynb ipython notebook file.

### Setup

Install leiningen from http://leiningen.org/

### Running

1. cd into scraper subfolder
2. run 
``` lein run [house|senate] [congressnum] [directory to download to] ```

Example:
``` lein run house 113 ../data ```

## word2vec ipython file

This is a ipython notebook file containing work perform for bill corpus of text work. The data is in datafile.zip or the scraper can optionally used to load it. This will need to be unziped into a subfolder called data to properly work, or change paths in the notebook.

## Comparison.py:

Description:
Imports the specified data based on the given starting and ending congress number.
Runs the FastGreedy, Walktrap, and Leading Eigenvector community detection algorithms
on the specified data and compares the resulting modularities between the different algorithms.

Usage:
python comparison.py &lt;house|senate&gt; &lt;starting_congress_number&gt; &lt;ending_congress_number&gt;

Valid Congress Session Numbers:
1 - 113 (I used Senate sessions 100 - 113 to complement the results obtained by cluster_igraph.py)

Check for output in:<br>
Leading Eigenvector Senate Clusters folder: the clusters produced by the Leading Eigenvector algorithm on Senate sessions 100 - 113

Walktrap Senate Clusters folder: the clusters produced by the Walktrap algorithm on Senate sessions 100 - 113

(FastGreedy graph results already produced by cluster_igraph.py)

comparison.png - A plot of the modularities produced for each outputed graph by the different algorithms. 

This program also prints the number of communities and the modularity scores
obtained by the different algorithms to the console.

Dependencies:
download_data.py (located in this directory)
igraph
sys
matplotlib.pyplot
