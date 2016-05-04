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

To create a corpus of text, a clojure app was made to scrape the websites and download the data. This does not have to be run. A zip called word2vec_datafile.zip has the corpus downloaded for the report. It is to be used with word2vec.ipynb ipython notebook file.

### Setup

Install leiningen from http://leiningen.org/

### Running

1. cd into scraper subfolder
2. run 
``` lein run [house|senate] [congressnum] [directory to download to] ```

Example:
``` lein run house 113 ../data ```

## word2vec ipython file

This is a ipython notebook file containing work perform for bill corpus of text work. The data is in word2vec_datafile.zip or the scraper can optionally used to load it. This will need to be unziped into a subfolder called data to properly work, or change paths in the notebook. The structure after unzipping should be like this in data folder, "data/109/*", "data/110/*", etc.

## Comparison.py:

**Description:**<br>
Imports the specified data based on the given starting and ending congress number.
Runs the FastGreedy, Walktrap, and Leading Eigenvector community detection algorithms
on the specified data and compares the resulting modularities between the different algorithms.

**Usage:**<br>
python comparison.py &lt;house|senate&gt; &lt;starting_congress_number&gt; &lt;ending_congress_number&gt;<br>

**Valid Congress Numbers:**<br>
1 - 113 (I used Senates 100 - 113 to complement the results obtained by cluster_igraph.py)<br>
(python comparison.py senate 100 113)

**Check for output in:**<br>
**Leading Eigenvector Senate Clusters folder:**<br> the clusters produced by the Leading Eigenvector algorithm on Senate sessions 100 - 113

**Walktrap Senate Clusters folder:**<br> the clusters produced by the Walktrap algorithm on Senate sessions 100 - 113

(FastGreedy graph results already produced by cluster_igraph.py)

**comparison.png** - A plot of the modularities produced for each outputed graph by the different algorithms. 

This program also prints the number of communities and the modularity scores
obtained by the different algorithms to the console.

**Dependencies:**<br>
download_data.py (located in this directory)<br>
igraph<br>
sys<br>
matplotlib.pyplot

## Cluster iGraph

Usage: ```python cluster_igraph.py (no params)```

The module gets house and senate data for 101 - 113 (approx 1990 - 2014) and computes clusters
using fast greedy modular optimization. The script compares modularity between the house vs senate,
and produces plots for each house/senate for 101 - 113.

## Visualization

In order to do the first part of the analysis to create the data 
 visualization, one can run the visualization_README as a bash script. 
 
 The following files must be in the directory with this script:
 ```
   download_data.py - This file defines functions used to download the data.
   savedata.py - This file downloads congress.pydata and saves it in 
                 the current directory so one does not need to download
                 the data for each run.
   visualization.py - This file saves 101 plots in a subdirectory plots/ in
                      the current directory. 
                      NOTE: One can edit this file to change the loadgraph
                      variable to True or False. If set to False, it will
                      load congress.pydata, create a graph of the senate,
                      and save it to allsenates.pydata. It will then run
                      as usual. Subsequent runs can have loadgraph set to
                      True, and the program will then load in the data from
                      allsenates.pydata and then run as usual. 
   makegif.sh - This file reduces files in plots/ to smaller *.png files 
                for further processing. These files are saved in a 
                subdirectory named smallerplots/ in the current directory.
                It then creates a gif from these smaller plots and saves it
                in the current directory as visualization.gif.
                ```

