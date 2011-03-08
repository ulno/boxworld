'''
Created on Mar 4, 2011

@author: ulno
'''

#import Inbox_Content.Inbox_Content as Inbox_Content
from Transport import Transport

from Queue import Queue

class Inbox(object): # TODO: must probably inherit from channel
    

    def __init__(self, queue_names):
        
        self.queue = Queue()

    
    def put(self, obj):
        '''
        Put an object (obj) in the box
        '''
        assert isinstance (obj, Transport), "only Transport allowed"
        self.queue.put(obj)
    
    def take(self):
        return self.queue.get(block=True)
        