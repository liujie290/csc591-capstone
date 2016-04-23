#!/usr/bin/python
from download_data import *
import pickle 

# Download all files.
allsenates = []
allhouses  = []
for congressnum in range(1,114):
  allhouses  += housedata(congressnum)
  allsenates += senatedata(congressnum)

# Save the data to disk so we do not have to download the data every time.
with open('congress.pydata', 'wb') as out:
  pickle.dump(allhouses,  out, pickle.HIGHEST_PROTOCOL)
  pickle.dump(allsenates, out, pickle.HIGHEST_PROTOCOL)

