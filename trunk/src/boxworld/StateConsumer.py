from Queue import Queue
from threading import Thread
from Geometry import Coord

class Frame:
    '''
    Represents global state for a point in time.
    '''
    
    def __init__(self, time, segment):
        self.time = time
        #print "Segment is %s" % str(segment)
        #print "Making values size %d" % segment.volume()
        self.values = [None] * segment.volume()
        self.size = segment.volume()
        self.populatedCount = 0
        self.segment = segment

    def __positionToOffset(self, pos):
        '''
        Non-collision hash of position to array offset.
        '''
        '''
        Normalize the position, relative to base coordinate of
        out segment
        '''
        normalizedPos = Coord(pos.x - self.segment.startCoord.x,
                              pos.y - self.segment.startCoord.y,
                              pos.z - self.segment.startCoord.z)
        dimensions = self.segment.dimensions()
        
        hash = normalizedPos.x + \
               dimensions.x * normalizedPos.y + \
               dimensions.x * dimensions.y * normalizedPos.z
               
        assert hash < dimensions.volume(),  "For segemnt %s and pos %s, normpos is %s and hash is %d and dimensions are %s" % (str(self.segment), str(pos), str(normalizedPos), hash, str(dimensions))

        return hash

    def setValue(self, pos, value):
            
        boxOffset = self.__positionToOffset(pos)
        #print "Setting pos: %s with offset %d, existing array is %s" %(str(pos), boxOffset, str(self.values))
        assert self.values[boxOffset] is None
        self.values[boxOffset] = value
        self.populatedCount += 1
        
    def isFull(self):
        return self.populatedCount == self.size

class State:
        
    def __init__(self, position, time, terpene):
        self.position = position
        self.time = time
        self.terpene = terpene

class StateConsumer(Thread):
    '''
    Consumes all Box states and sends to FileWriter in organized Frames.
    '''
    
    
    def __init__(self, fileWriter, endTime, segment):
        Thread.__init__(self)
        self.fileWriter = fileWriter
        self.stateQueue = Queue()
        self.endTime = endTime
        self.segment = segment
        self.frameSize = segment.volume()
        
    def register(self, box):
        self.stateQueue.put(State(box.position, 
                                  box.time, 
                                  box.terpene_concentration))
        
    def run(self):
        
        self.work = True
        
        frames = {} # indexed by time
        
        while True:
            state = self.stateQueue.get()
            if not frames.has_key(state.time):
                frames[state.time] = Frame(state.time, self.segment)
            
            frames[state.time].setValue(state.position, state.terpene)
            
            if frames[state.time].isFull():
                #print "Printing frame for time %d, end time is %d" % (state.time, self.endTime)
                self.fileWriter.write(frames[state.time])
                # Frames can be large, and are not needed after printing.
                del frames[state.time]
                #Test if we are completely done
                if state.time == self.endTime:
                    self.fileWriter.close()
                    break
        
        