#!/usr/bin/python
from download_data import *
import pickle 

# Download all files.
allsenates = []
allhouses  = []
for congressnum in range(1,114):
  allhouses  += housedata(congressnum)
  allsenates += senatedata(congressnum)

with open('congress.pydata', 'wb') as out:
  pickle.dump(allhouses,  out, pickle.HIGHEST_PROTOCOL)
  pickle.dump(allsenates, out, pickle.HIGHEST_PROTOCOL)
"""
print "Making graphs..."
housegraph = makegraph(allhouses)
senategraph = makegraph(allsenates)

print "Saving graphs..."
housegraph.write_pickle('allhouses.pydata')
senategraph.write_pickle('allsenates.pydata')
"""
