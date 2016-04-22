Usage: python cluster_igraph.py (no params)

The module gets house and senate data for 101 - 113 (approx 1990 - 2014) and computes clusters
using fast greedy modular optimization. The script compares modularity between the house vs senate,
and produces plots for each house/senate for 101 - 113.

-----------------
Required Modules:
download_data.py
matplotlib.pyplot
igraph
numpy
collections
