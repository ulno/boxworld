from Queue import Queue
from threading import Thread

class Frame:
    '''
    Represents global state for a point in time.
    '''
    
    def __init__(self, time, segment):
        self.time = time
        self.values = {}
        self.size = segment.volume()
        self.populatedCount = 0
        self.segment = segment

    def setValue(self, pos, value):
            
        assert not self.values.has_key(pos)
        self.values[pos] = value
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
        
        