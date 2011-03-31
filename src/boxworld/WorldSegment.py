import re
from .Source import Source
from .Chemical_Sink import Chemical_Sink

class WorldSegmentFactory:
    
    def __init__(self, worldSize, fileName):
        assert worldSize > 0
        assert fileName is not None
        
        self.worldSize = worldSize
        self.fileName = fileName
        self.sources = []
        self.sinks = []
        self.boxes = []


        self.importFromFile()

    COMMENT_REGEX = "(#.*)?$" #defined as optional
    EMPTY_LINE_REGEX = "\s*" + COMMENT_REGEX
    TIME_START_REGEX = "time_start\s+(\d+)" + COMMENT_REGEX
    TIME_END_REGEX = "time_end\s+(\d+)" + COMMENT_REGEX
    TIME_DELTA_REGEX = "time_delta\s+(\d+)" + COMMENT_REGEX
    
    SOURCE_REGEX = "(\d+),(\d+),(\d+)\s*" + COMMENT_REGEX
    
    SINK_REGEX = "(\d+),(\d+),(\d+),(\d+),(\d+)\s*" + COMMENT_REGEX

    #Parse States
    PARSE_WORLD_SETTING = 'parseWorldSetting'
    PARSE_SINK = 'parseSink'
    PARSE_SOURCE = 'parseSource'
    PARSE_BOX = 'parseBox'

    def importFromFile(self):
        '''
        Import a complete world definition from a text file.
        If a single syntax error occurs, the process is halted and an exception raised.
        '''
        
        file = open(self.fileName, 'r')
        
        self.parseState = 'parseWorldSetting'
        
        for line in file:
            if re.match(self.EMPTY_LINE_REGEX, line):
                continue
            elif self.parseChangeState(line):
                continue
            if self.parseState == 'parseWorldSetting':
                self.parseWorldSetting(line)
            elif self.parseState == 'parseSource':
                self.parseSource(line)
            elif self.parseState == 'parseSink':
                self.parseSink(line)
            elif self.parseState == 'parseBox':
                self.parseBox(line)
            else:
                raise Exception("Could not parse line='%s'" % line)
            
    def parseSink(self, line):        
        m = re.match(self.SINK_REGEX, line)
        if not m:
            raise Exception("Illegal source syntax in line = '%s'" % line)
        
        self.sinks.append(Chemical_Sink(int(m.group(1)), int(m.group(2)), int(m.group(3)), 
                                   int(m.group(4)), int(m.group(5))))
    
    
    def parseChangeState(self, line):
        '''
        Change state and return True if state change. 
        Else, return False.
        '''
        states = {"sources": self.PARSE_SOURCE,
                  "sinks": self.PARSE_SINK,
                  "boxes": self.PARSE_BOX}

        for (name,state) in states.items():
            if re.match("\s*" + name + "_start\s*" + self.COMMENT_REGEX, line):
                self.parseState = state
                return True
            elif re.match("\s*" + name + "_end\s*" + self.COMMENT_REGEX, line):
                self.parseState = self.PARSE_WORLD_SETTING
                return True
        
        return False
    
    def parseSource(self, line):
        
        m = re.match(self.SOURCE_REGEX, line)
        if not m:
            raise Exception("Illegal source syntax in line = '%s'" % line)
        
        self.sources.append(Source(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    
    def parseWorldSetting(self, line):
        if re.match(self.EMPTY_LINE_REGEX, line):
                return
            
        m = re.match(self.TIME_START_REGEX, line)
        if m:
            self.timeStart = int(m.group(1))
            return
            
        m = re.match(self.TIME_END_REGEX, line)
        if m:
            self.timeEnd = int(m.group(1))
            return
            
        m = re.match(self.TIME_DELTA_REGEX, line)
        if m:
            self.timeDelta = int(m.group(1))
            return   
        
    def getWorldSegment(self, rank):
        assert rank >= 0 and rank < self.worldSize



class WorldSegment:
    
    def __init__(self, rank, worldSize, boxes):
        assert rank > worldSize
        assert len(boxes) > 0
        
        self.rank = rank
        self.worldSize = worldSize
        self.boxes = boxes
    
    def run(self):
        
        self.boxThreads = []
        for box in self.boxes():
            self.boxThreads.append(box.run())
            
        for t in self.boxThreads:
            t.join()