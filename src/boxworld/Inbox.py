'''
Created on Mar 4, 2011

@author: ulno
'''

#import Inbox_Content.Inbox_Content as Inbox_Content
from MpiChannel import Envelope

from Transport import Transport

from Queue import Queue
    
class LocalInbox(): # TODO: must probably inherit from channel
    

    def __init__(self):
        
        self.queue = Queue()

    
    def put(self, obj):
        '''
        Put an object (obj) in the box
        '''
        assert isinstance (obj, Transport), "only Transport allowed"
        self.queue.put(obj)
    
    def take(self):
        return self.queue.get(block=True)
    
class RemoteInbox():
    

    def __init__(self, srcCoords, destCoords, mpiChannel):
        
        self.srcCoords = srcCoords
        self.destCoords = destCoords
        self.mpiChannel = mpiChannel

    
    def put(self, obj):
        #print ("Sending from %s to %s" %(str(self.srcCoords), str(self.destCoords)))
        self.mpiChannel.send(Envelope(self.srcCoords, self.destCoords, obj))
    
    def take(self):
        assert False, "Trying to take from remote"
        