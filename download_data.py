#!/usr/bin/python
import urllib2
import numpy as np
import math
import igraph

def getdata(url):
  """
  usage: getdata(url)
  returns: A list of tuples. The first tuple is a header. The rest are records
           that were downloaded. 
   See, e.g., http://voteview.com/house113.htm for example data. 
   1.  Congress Number
   2.  ICPSR ID Number:  5 digit code assigned by the ICPSR as 
                       corrected by Howard Rosenthal and myself.
   3.  State Code:  2 digit ICPSR State Code. 
   4.  Congressional District Number (0 if Senate)
   5.  State Name
   6.  Party Code:  100 = Dem., 200 = Repub. (See PARTY3.DAT)
   7.  Occupancy:  ICPSR Occupancy Code -- 0=only occupant; 1=1st occupant; 2=2nd occupant; etc.
   8.  Last Means of Attaining Office:  ICPSR Attain-Office Code -- 1=general election;
                2=special election; 3=elected by state legislature; 5=appointed
   9.  Name
  10 - to the number of roll calls + 10:  Roll Call Data --
               0=not a member, 1=Yea, 2=Paired Yea, 3=Announced Yea,
               4=Announced Nay, 5=Paired Nay, 6=Nay,
               7=Present (some Congresses, also not used some Congresses),
               8=Present (some Congresses, also not used some Congresses),
               9=Not Voting  
  """
  # The roll calls are in a (mostly) fixed width format, where the name field
  # is at least 10 characters, but can be longer. 
  fieldlens = (3,5,2,2,7,4,1,1,10)

  data = []
  for line in urllib2.urlopen(url):
    #print line
    # Rec will hold a tuple of the ten data elements.
    rec = [None]*10
    pos = 0 # Current position in the line.
    for fieldnum,fieldlen in enumerate(fieldlens):
      rec[fieldnum] = line[pos:pos+fieldlen]
      pos+=fieldlen
    votes = line[pos:].strip()
    #print rec
    #print votes
    # We change yays to 1, nays to -1, and other to 0.
    # Some names are over 10 characters and run into the votes field, so
    # we ignore non-numeric characters.
    rec[9] = np.array([1 if 1 <= int(vote) and int(vote) <= 3 
                         else (-1 if 4 <= int(vote) and int(vote) <= 6 
                         else 0) \
                       for vote 
                       in votes
                       if vote in '0123456789'
                       ])
    data.extend([tuple(rec)])
  return data

def housedata(congressnum
             ,baseurl='ftp://voteview.com/dtaord/hou'
             ,tailurl='kh.ord'):
  url = baseurl + str(congressnum).zfill(2) + tailurl
  print "Downloading house roll call data from congress",str(congressnum), \
        "from",url
  data = getdata(url)
  return data

def senatedata(congressnum
             ,baseurl='ftp://voteview.com/dtaord/sen'
             ,tailurl='kh.ord'):
  url = baseurl + str(congressnum).zfill(2) + tailurl
  print "Downloading senate roll call data from congress",str(congressnum), \
        "from",url
  data = getdata(url)
  return data

def makegraph(data, allownegweights=False):
  """
  Usage: makegraph(data) where data is from housedata(N), senatedata(N), or
         combined data (e.g., housedata(N)+housedata(N-1)+...). It can
         optionally be passed makegraph(data, allownegweights=True), in 
         which case it will produce a graph that has both positive weights
         for people that vote together and negative weights for people that
         vote in an opposite fashion. 
  Returns: An igraph graph. Edge attributes include the cosine similarity 
           between two congressmen if the two ever voted on the same issue.
           The cosine similariy is stored in the "weight" attribute of the 
           edge. If the two never voted on the same issue, there will be no
           edge between them. Additionally, if allownegweights is given its 
           default value of False, there will only be edges if the two vote
           the same way more than half the time. Each vertex has an "info" 
           attribute that has attribute information that can be accessed with, 
           e.g.,
                graph.vs[0]["info"].party
           Attribute information includes 
                id - The ICPSR ID Number for the represenative or senator
                vertexid - The vertex id (this is redudant)
                congresses - A set of all congresses the congressman was in
                state - A set of all states the congressman represented
                district - A set of all districts the congressman represented,
                           where a district may not be unique across states.
                statename - A set of all states the congressman represented in
                            abbreviated word form (the other state is an id)
                party - A set of all party IDs the congressman had
                occupancy - A set of all occupancy codes the congressman had
                howattained - A set of all the ways the congressman was elected
                name - A set of all names for the congressman in the files
  """
  # The first two fields in the data serve as the primary key:
  # 1.  Congress Number
  # 2.  ICPSR ID Number
  # 3.  State Code
  # 4.  Congressional District Number (0 if Senate)
  # 5.  State Name
  # 6.  Party Code
  # 7.  Occupancy
  # 8.  Last Means of Attaining Office
  # 9.  Name
  #10.  Roll call
  class info:
    def __init__(self,rec,vertexid):
      self.id = rec[1]
      self.vertexid = vertexid
      self.congresses = set([rec[0]])
      self.state = set([rec[2]])
      self.district = set([rec[3]])
      self.statename = set([rec[4]])
      self.party = list([rec[5]])
      self.occupancy = set([rec[6]])
      self.howattained = set([rec[7]])
      self.name = set([rec[8]])
    def addinfo(self,rec):
      self.congresses = self.congresses.union([rec[0]])
      self.state = self.state.union([rec[2]])
      self.district = self.district.union([rec[3]])
      self.statename = self.statename.union([rec[4]])
      self.party = self.party+list([rec[5]])
      self.occupancy = self.occupancy.union([rec[6]])
      self.howattained = self.howattained.union([rec[7]])
      self.name = self.name.union([rec[8]])
  attrbyid = {} # Holds attributes by ICPSR ID.
  votebypk = {} # Holds votes by (congress number, ICPSR ID) tuple.
  vertexid = 0
  for rec in data:
    #print rec
    votebypk[(rec[0], rec[1])] = rec[9]
    if rec[1] in attrbyid.keys():
      attrbyid[rec[1]].addinfo(rec)
    else:
      attrbyid[rec[1]] = info(rec,vertexid)
      vertexid += 1
  # Calculate cosine similarity between pairs of ICPSR IDs.
  sim = {}
  for id1 in attrbyid.keys():
    for id2 in attrbyid.keys():
      if id1 < id2:
        commonvotes = 0
        numvotes1 = 0
        numvotes2 = 0
        for congress in \
               attrbyid[id1].congresses.intersection(attrbyid[id2].congresses):
          commonvotes += np.dot(votebypk[(congress,id1)] \
                              ,votebypk[(congress,id2)])
          numvotes1 += np.sum(votebypk[(congress,id1)] != 0)
          numvotes2 += np.sum(votebypk[(congress,id2)] != 0)
        if numvotes1*numvotes2 == 0:
          sim[(id1,id2)] = None # In this case, we won't draw an edge.
        else:
          sim[(id1,id2)] = commonvotes / math.sqrt(numvotes1*numvotes2)

  # Use data to create graph.
  network = igraph.Graph()
  network.add_vertices(len(attrbyid.keys()))
  edgeid = 0
  for id1,id2 in sim.keys():
    if sim[id1,id2] != None and (allownegweights or 0 < sim[id1,id2]):
      edge_list = []
      edge_list.append((attrbyid[id1].vertexid, attrbyid[id2].vertexid))
      network.add_edges(edge_list)
      network.es[edgeid]["weight"] = sim[(id1,id2)]
      edgeid+=1
  for id1 in attrbyid.keys():
    network.vs[attrbyid[id1].vertexid]["info"] = attrbyid[id1]

  return network

def print_to_spark_file(graph, filename):
  # write  file for use by spark...need a distance metric between all pairs of
  # congressmen...which will be 1 - cosine_sim, or 1 if there is no edge
  # for now just use vertex id as the mapping...we can change later
  
  f=open(filename, 'w')
  f.write("%d\n"%(len(graph.vs)))
  for i in range(0, len(graph.vs)-1):
    for j in range(i+1, len(graph.vs)):
      edge=graph.get_eid(i,j,error=False)
      weight=0
      if edge != -1:
        weight=graph.es[edge]["weight"]
# need to flip from a similarity to a distance
      weight = 1 - weight
      f.write("%d %d %f\n" % (i,j,weight))

if __name__ == "__main__":
  somedata = housedata(1)+housedata(2)+housedata(3)+housedata(4)
  agraph = makegraph(somedata)

  somemoredata = senatedata(113)
  anothergraph = makegraph(somemoredata)

  print_to_spark_file(agraph, "house_data.txt")
