'''
Created on Mar 18, 2011

@author: willmore
'''

from threading import Thread

from Inbox import RemoteInbox

class RemoteBox:
    
    def __init__(self, coords, mpiChannel, remoteManager):
        self.coords = coords
        self.mpiChannel = mpiChannel
        self.remoteManager = remoteManager

        #will send messages through MPI
        self.up_inbox = RemoteInbox((coords[0], coords[1], coords[2]+1), self.coords, mpiChannel)
        self.down_inbox = RemoteInbox((coords[0], coords[1], coords[2]-1), self.coords, mpiChannel)
        self.left_inbox = RemoteInbox((coords[0]-1, coords[1], coords[2]), self.coords, mpiChannel)
        self.right_inbox = RemoteInbox((coords[0]+1, coords[1], coords[2]), self.coords, mpiChannel)
        self.front_inbox = RemoteInbox((coords[0], coords[1]-1, coords[2]), self.coords, mpiChannel)
        self.back_inbox = RemoteInbox((coords[0], coords[1]+1, coords[2]), self.coords, mpiChannel)

        self.up_outbox = None
        self.down_outbox = None
        self.left_outbox = None
        self.right_outbox = None
        self.front_outbox = None
        self.back_outbox = None


    def run(self):
        
        #Wire our "real" neighbors' inboxes to remote connection manager
        coords = self.coords
        
        if self.up_outbox is not None:
            self.remoteManager.register((coords[0], coords[1], coords[2]+1), self.up_outbox)
            
        if self.down_outbox is not None:
            self.remoteManager.register((coords[0], coords[1], coords[2]-1), self.down_outbox)
            
        if self.left_outbox is not None:
            self.remoteManager.register((coords[0]-1, coords[1], coords[2]), self.left_outbox)
            
        if self.right_outbox is not None:
            self.remoteManager.register((coords[0]+1, coords[1], coords[2]), self.right_outbox)
            
        if self.front_outbox is not None:
            self.remoteManager.register((coords[0], coords[1]-1, coords[2]), self.front_outbox)
            
        if self.back_outbox is not None:
            self.remoteManager.register((coords[0], coords[1]+1, coords[2]), self.back_outbox)
            

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