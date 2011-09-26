

class FileWriter(object):
    '''
    Consumes Frame and serializes to disk.
    '''
    
    def __init__(self, fileName, segment):
        self.fileName = fileName
        self.file = open(fileName, 'w')
        self.segment = segment
        
        self.file.write("SEGMENT %d,%d,%d %d,%d,%d\n" % (segment.startCoord.x, 
                                                        segment.startCoord.y, 
                                                        segment.startCoord.z,
                                                        segment.endCoord.x, 
                                                        segment.endCoord.y, 
                                                        segment.endCoord.z))
        
    def write(self, frame):
        '''
        Write a 'Frame' to disk. A Frame constitutes the time and all cell values.
        '''
        self.file.write("START FRAME %f\n" % frame.time)
        
        for coord in frame.segment.coorditer():
            self.file.write("%d\n" % frame.values[coord])
        
        self.file.write("END FRAME %f\n" % frame.time)
        
    def close(self):
        self.file.close()