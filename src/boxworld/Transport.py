'''
Created on Mar 4, 2011
These objects will be put into the inboxes of the respective neighboring boxes

@author: ulno
'''

class Transport(object):
    '''
    classdocs
    '''


    def __init__(self, prev_state, delta):
        '''
        Constructor
        '''
        self.prev_state = prev_state
        self.delta = delta
        # Later we might have specific terpenes here