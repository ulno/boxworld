'''
Created on Mar 17, 2011

@author: willmore
'''
from mpi4py import MPI

class Envelope:
    
    def __init__(self, src, to, msg):
        self.src = src
        self.to = to
        self.msg = msg

class MpiChannel:
    
    comm = MPI.COMM_WORLD #is this threadsafe?
    
    def __init__(self, remoteRank):
        self.remoteRank = remoteRank
        
    def send(self, envelope):
        MpiChannel.comm.send(envelope, dest=self.remoteRank)
        
    def receive(self):
        return MpiChannel.comm.recv(source=self.remoteRank)
    
class MpiChannelFactory:
    
    def __init__(self, boxRankMap):
        # Mapping object from coordinates to MPI rank
        self.boxRankMap = boxRankMap
        self.rankChannelMap = {}
        
    def getKnownMpiChannels(self):
        return self.rankChannelMap.values()   
        
    def getMpiChannel(self, coords):
        #Lazy load channel
        rank = self.boxRankMap.getRank(coords)
       
        if not self.rankChannelMap.has_key(rank):
            self.rankChannelMap[rank] = MpiChannel(rank)
            
        return self.rankChannelMap[rank]    
        