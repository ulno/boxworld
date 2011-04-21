

class FileWriter:
    '''
    Consumes Frame and serializes to disk.
    '''
    
    
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = open(fileName, 'w')
        
    def write(self, frame):
        '''
        Write a 'Frame' to disk. A Frame constitutes the time and all cell values.
        '''
        
        self.file.write("START FRAME %f" % frame.time)
        
        for value in frame.values:
            self.file.write(str(value))
        
        self.file.write("END FRAME %f" % frame.time)