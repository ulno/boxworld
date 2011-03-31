import re

class WorldSegmentFactory:
    
    def __init__(self, worldSize, fileName):
        assert worldSize > 0
        assert fileName is not None
        
        self.worldSize = worldSize
        self.fileName = fileName

        self.importFromFile()

    COMMENT_REGEX = "#?\.*$" #defined as optional
    EMPTY_LINE_REGEX = "\s" + COMMENT_REGEX
    TIME_START_REGEX = "time_start\s+(\d+)" + COMMENT_REGEX
    TIME_END_REGEX = "time_end\s+(\d+)" + COMMENT_REGEX
    TIME_DELTA_REGEX = "time_delta\s+(\d+)" + COMMENT_REGEX

    def importFromFile(self):
        
        file = open(self.fileName, 'r')
        
        self.parseState = 'parseWorldSetting'
        
        for line in file:
            if self.parseState == 'parseWorldSetting':
                self.parseWorldSetting(line)
            elif self.parseState == 'parseSource':
                self.parseSource(line)
            elif self.parseState == 'parseSink':
                self.parseSink(line)
            elif self.parseState == 'parseBox':
                self.parseBox(line)
            elif self.changeParseState(line):
                continue
            elif re.match(self.EMPTY_LINE_REGEX, line):
                continue 
            else:
                raise Exception("Could not parse line='%s'" % line)
            
    
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