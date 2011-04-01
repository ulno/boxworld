'''
Created on Mar 18, 2011

@author: willmore
'''

from threading import Thread

from Inbox import RemoteInbox

class RemoteBox:
    
    def __init__(self, position, mpiChannel, remoteManager):
        self.position = position
        self.mpiChannel = mpiChannel
        self.remoteManager = remoteManager

        #will send messages through MPI
        
        self.inboxes = {}
        
        for n in self.position.surroundingCoords():
            self.inboxes[n] = RemoteInbox(n, self.position, mpiChannel)

        self.outboxes = {}

    def run(self):
        pass
       
    def connect(self, neighbor):
        '''
        Wire our "real" neighbors' inboxes to remote connection manager.
        '''
        
        p = neighbor.position     
        self.remoteManager.register((p.x, p.y, p.z), neighbor.inboxes[self.position])     

class RemoteBoxFactory:
    
    def __init__(self, mpiChannelFactory, remoteManager):
        self.mpiChannelFactory = mpiChannelFactory
        self.remoteManager = remoteManager
        
    def getBox(self, coords):
        return RemoteBox(coords, self.mpiChannelFactory.getMpiChannel(coords), self.remoteManager)
    

class RemoteManager:
    '''
    Listen for MPI messages, passing them based on the envelope to proper inbox.
    '''
    
    def __init__(self, mpiChannelFactory):
        self.inboxes = {}
        self.mpiChannelFactory = mpiChannelFactory
    
    def register(self, coords, inbox):
        print "Register coord %s" % str(coords)
        self.inboxes[coords] = inbox
    
    def run(self):
        
        self.listen = True
        threads = []
        for channel in self.mpiChannelFactory.getKnownMpiChannels():
            t = Thread(target=self.__listen, args=(channel,))
            t.start()
            threads.append(t)
            
        return threads
    
    def stop(self):
        #Notify listening threads to end
        self.listen = False
        
    def __listen(self, channel):
        
        while self.listen:
            env = channel.receive()
            self.inboxes[env.to].put(env.msg)