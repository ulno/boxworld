'''
Created on Apr 26, 2011

@author: willmore
'''

from Geometry import Segment, Coord
import string
import re

class FrameFileJoiner(object):

    def __init__(self, files):
        self.files = files
        
    def __getSegment(self, file):
        file.seek(0)
        
        while True:
            line = file.readline()
            m = re.search('SEGMENT (\d+),(\d+),(\d+) (\d+),(\d+),(\d+)', line)  
             
            if m:
                return Segment(Coord(int(m.group(1)), int(m.group(2)), int(m.group(3))),
                               Coord(int(m.group(4)), int(m.group(5)), int(m.group(6))))
                               
        raise Exception("Did not find segment definition")
    
    def __getFrameData(self, file, timestep):
        file.seek(0)
                
        regex = "START FRAME %d" % timestep
        
        while True:
            m = re.search(regex, file.readline())
            if m:                
                out = []
                while True:
                    line = file.readline().strip()
                    if re.search("END FRAME", line):
                        return out
                    out.append(line)   
            
        raise Exception("Could not find frame")
        
    def getFrameAsVTK(self, timestep):
        
        coordDataMap = {}
        
        # We don't have the world geometry in the slice files, so guess.
        minCoord = None
        maxCoord = None
        
        
        for file in self.files:
            segment = self.__getSegment(file)
            data = self.__getFrameData(file, timestep)
            
            i = 0
            for coord in segment.coorditer():
                
                minCoord = self.__min(minCoord, coord) if minCoord is not None else coord
                maxCoord = self.__max(maxCoord, coord) if maxCoord is not None else coord
                
                assert not coordDataMap.has_key(coord), "Map already has coord %s" % str(coord)
                coordDataMap[coord] = data[i]
                i += 1
                
        worldSegment = Segment(minCoord, maxCoord)
        
        
        vtkLines = []
        yLine = 0 
        currLine = []
        for coord in worldSegment.vtkCoordIter():
            
            assert coordDataMap.has_key(coord), "Cannot find coord %s" % str(coord)
            
            if yLine != coord.y:
                vtkLines.append(string.join(currLine, " "))
                currLine = []
                yLine = coord.y
                
            currLine.append(coordDataMap[coord])
            
        #Append last line
        vtkLines.append(string.join(currLine, " "))
        
        vtkHeaders = []
        vtkHeaders.append("# vtk DataFile Version 2.0")
        vtkHeaders.append("BoxWorld data for time %d" % timestep)
        vtkHeaders.append("ASCII\n")
        vtkHeaders.append("DATASET STRUCTURED_POINTS")
        
        dimensions = worldSegment.dimensions()
        vtkHeaders.append("DIMENSIONS    %d   %d   %d" % (dimensions.x, dimensions.y, dimensions.z))
        vtkHeaders.append("ORIGIN    0.000   0.000   0.000")
        vtkHeaders.append("SPACING    1.000   1.000   1.000\n")
        vtkHeaders.append("POINT_DATA   %d" % worldSegment.volume())
        vtkHeaders.append("SCALARS scalars float")
        vtkHeaders.append("LOOKUP_TABLE default\n")
        
        vtkFile = []
        vtkFile.extend(vtkHeaders)
        vtkFile.extend(vtkLines)
        
        return string.join(vtkFile, "\n")


                
    def __min(self, c1, c2):
        if c1.x <= c2.x and c1.y <= c2.y and c1.z <= c2.z:
            return c1
        return c2
    
    def __max(self, c1, c2):
        if c1.x >= c2.x and c1.y >= c2.y and c1.z >= c2.z:
            return c1
        return c2
            