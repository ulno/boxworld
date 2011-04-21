from Queue import Queue
from threading import Thread


class Frame:
    '''
    Represents global state for a point in time.
    '''
    
    def __init__(self, time, size):
        self.time = time
        self.values = [None] * size
        self.size = size
        self.populatedCount = 0

    def __positionToOffset(self, pos):
        '''
        Non-collision hash of position to array offset.
        TODO move array offset to/from conversion to Coord
        '''
        return pos.x + \
               self.worldDimensions.x * pos.y + \
               self.worldDimensions.x * self.worldDimensions.y * pos.z

    def setValue(self, pos, value):
            
        boxOffset = self.__positionToOffset(pos)
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
    
    
    def __init__(self, fileWriter, endTime, worldDimensions):
        Thread.__init__(self)
        self.fileWriter = fileWriter
        self.stateQueue = Queue()
        self.endTime = endTime
        self.worldDimensions = worldDimensions
        self.frameSize = worldDimensions.volume()
        
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
                frames[state.time] = Frame(state.time, self.frameSize)
            
            frames[state.time].setValue(state.position, state.terpene)
            
            if frames[state.time].isFull():
                self.fileWriter.printFrame(frames[state.time])
                # Frames can be large, and are not needed after printing.
                del frames[state.time]
        