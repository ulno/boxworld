import re
import copy

from .Source import Source
from .Chemical_Sink import Chemical_Sink
from .Geometry import Dimensions
from .Geometry import Coord
from .Box import Box
from .RemoteBox import RemoteBoxFactory
from .RemoteBox import RemoteManager
from .RankMap import RankMapGenerator
from .MpiChannel import MpiChannelFactory
from .Geometry import Segment
from .StateConsumer import StateConsumer
from .FIleWriter import FileWriter


class WorldSegmentFactory:
    
    def __init__(self, worldSize, fileName):
        assert worldSize > 0
        assert fileName is not None
        
        self.worldSize = worldSize
        self.fileName = fileName
        self.sources = []
        self.sinks = []
        self.boxes = {}
        self.lightFuncs = {}
        self.tempFuncs = {}
        
        self.importFromFile()
        
        self.rankMap = RankMapGenerator().generate(self.worldSize, self.dimensions)
        

    COMMENT_REGEX = "\s*(#.*)?$" #defined as optional
    EMPTY_LINE_REGEX = COMMENT_REGEX
    TIME_START_REGEX = "time_start\s+(\d+)" + COMMENT_REGEX
    TIME_END_REGEX = "time_end\s+(\d+)" + COMMENT_REGEX
    TIME_DELTA_REGEX = "time_delta\s+(\d+)" + COMMENT_REGEX
    OUTPUT_FILE_REGEX = "output_file\s+(\w+)" + COMMENT_REGEX
    CUBE_SIZE_REGEX = "cube_size\s+(\d+)" + COMMENT_REGEX
    DIMENSIONS_REGEX = "dimensions\s+(\d+),(\d+),(\d+)\s*" + COMMENT_REGEX
    
    LIGHT_FUNC_REGEX = "light_function\s+(\w+)\s+(lambda.+)"
    TEMP_FUNC_REGEX = "temperature_function\s+(\w+)\s+(lambda.+)"
    
    
    
    SOURCE_REGEX = "(\d+),(\d+),(\d+)\s*" + COMMENT_REGEX
    
    SINK_REGEX = "(\d+),(\d+),(\d+),(\d+),(\d+)\s*" + COMMENT_REGEX

    BOX_REGEX = "(\d+),(\w+),(\w+)\s*" + COMMENT_REGEX

    

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
        
        self.currentCoord = Coord(0,0,0)
        
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
           
    def parseBox(self, line):    
        m = re.match(self.BOX_REGEX, line)
        if not m:
            raise Exception("Illegal Box syntax in line = '%s'" % line)
    
        tempFunc = self.tempFuncs[m.group(3)]
        lightFunc = self.lightFuncs[m.group(2)]
        
        self.boxes[self.currentCoord] = Box(self.currentCoord, self.cubeSize, lightFunc, 
                                             tempFunc,self.timeDelta, self.timeStart, 
                                             self.timeEnd, int(m.group(1))) 
        #bprint "Adding %s" % str(self.currentCoord)
    
        # Increment coordinate for next parsed box
        # The increment order in x, then y, then z. 
        # The values wrap in that order when they hit the max, as defined by self.dimensions   
        oldCoord = self.currentCoord
        self.currentCoord = copy.copy(oldCoord)
        self.currentCoord.x = (oldCoord.x + 1) % self.dimensions.x
        if self.currentCoord.x == 0:
            self.currentCoord.y = (oldCoord.y + 1) % self.dimensions.y
            if self.currentCoord.y == 0:
                # Z is the last to increment and thus should never wrap (except for very last iteration which is disregarded)
                self.currentCoord.z = oldCoord.z + 1
                
        
            
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
        
        m = re.match(self.OUTPUT_FILE_REGEX, line)
        if m:
            self.outFileName = m.group(1)
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
        
        m = re.match(self.CUBE_SIZE_REGEX, line)
        if m:
            self.cubeSize = int(m.group(1))
            return
        
        m = re.match(self.DIMENSIONS_REGEX, line)
        if m:
            self.dimensions = Dimensions(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            return
        
        m = re.match(self.LIGHT_FUNC_REGEX, line)
        if m:
            self.lightFuncs[m.group(1)] = eval(m.group(2))
            return
        
        m = re.match(self.TEMP_FUNC_REGEX, line)
        if m:
            self.tempFuncs[m.group(1)] = eval(m.group(2))
            return
        
    def getWorldSegment(self, rank):
        '''
        Given a valid MPI rank, returns the corresponding WorldSegment.
        '''
        
        assert rank >= 0 and rank < self.worldSize, "Invalid rank %d for world size %d" % (rank, self.worldSize)
        segment = self.rankMap.getSegment(rank)
        boxes = {}
        for coord in segment.coorditer():
            boxes[coord] = self.boxes[coord]

        return WorldSegment(rank, self.worldSize, self.dimensions, 
                            segment, boxes, self.rankMap, self.outFileName)

class WorldSegment:
    '''
    A 3D rectangular collection of connected boxes within the world.
    '''
    
    def __init__(self, rank, worldSize, worldDimensions, 
                 segment, boxes, rankMap, outFileName):
        
        assert rank < worldSize, "%d not < %d" % (rank, worldSize)
        assert len(boxes) > 0
        
        self.rank = rank
        self.worldSize = worldSize
        self.boxes = boxes
        self.segment = segment
        self.worldArea = Segment(Coord(0,0,0), Coord(worldDimensions.x-1, worldDimensions.y-1, worldDimensions.z-1))
        
        self.remoteChannelFactory = MpiChannelFactory(rankMap)
        self.remoteManager = RemoteManager(self.remoteChannelFactory) 
        self.remoteBoxFactory = RemoteBoxFactory(self.remoteChannelFactory, self.remoteManager)
        
        self.stateConsumer = StateConsumer(FileWriter("%s-%d.txt" % (outFileName, self.rank), self.segment), 
                                           boxes.values()[0].end_time, #hack 
                                           self.segment)
        
        # Wire the local boxes together, and wire local with remote boxes.
        for (coord, box) in boxes.iteritems():
            
            box.stateConsumer = self.stateConsumer
            
            
            #print "Connection box: %s" % coord
            for n in coord.surroundingCoords():
                if self.segment.contains(n):
                    #print "\tAdding local neighbor %s" % n
                    box.connect(boxes[n])
                elif self.worldArea.contains(n):
                    #Each remote box will be connected to one and one local box
                    #print "\tAdding remote neighbor %s" % n
                    rb = self.remoteBoxFactory.getBox(n)
                    box.connect(rb)
                    rb.connect(box)
                    
    
    def run(self):
        '''
        Run the experiment for the boxes contained in this world segment.
        This call blocks until all boxes have fully executed.
        '''
        print "Starting Remote Manager"
        self.remoteManager.run()
        
        print "Starting State Consumer"
        self.stateConsumer.start()
        
        print "Starting Boxes"
        
        self.boxThreads = []
        for box in self.boxes.values():
            self.boxThreads.append(box.run())
            
        for t in self.boxThreads:
            t.join()
            
        print "Joining on state consumer"
        self.stateConsumer.join()
        
        print "Stopping remoteManager"
        self.remoteManager.stop()