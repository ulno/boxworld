'''
Created on Mar 21, 2011

@author: willmore
'''

from .Geometry import Coord
from .Geometry import Segment

class Split(object):
    
    def __init__(self, x, y, z):
        
        assert x > 0
        assert y > 0
        assert z > 0
        
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):    
        return "[x=%d y=%d z=%d]" % (self.x, self.y, self.z)

class RankMapGenerator(object):
    
    def generate(self, worldSize, dimensions):
        split = self._idealSplit(worldSize, dimensions)
        return RankMap(worldSize, dimensions, split)            
        
    
    def _idealSplit(self, worldSize, dimensions):
        
        idealSplit = None
        idealSurfaceArea = None #surface area between all cells
        
        for xCount in range(1, dimensions.x + 1):
            for yCount in range(1, dimensions.y + 1):
                if xCount*yCount > worldSize:
                    break
                
                for zCount in range(1, dimensions.z + 1):
                    
                    if xCount*yCount*zCount != worldSize:
                        continue
                    elif xCount*yCount*zCount != worldSize:
                        break
                   
                    surfaceArea = self._calculateSurfaceArea(dimensions, xCount, yCount, zCount)

                    if idealSurfaceArea is None or surfaceArea < idealSurfaceArea:
                        idealSplit = Split(xCount, yCount, zCount)
                        idealSurfaceArea = surfaceArea
                        
        return idealSplit   
    
    def _calculateSurfaceArea(self, dimensions, xCount, yCount, zCount): 
        '''
        Calculate the area of communication between all the cells, returned in number
        of square faces.
        '''     
        
        return dimensions.z * dimensions.y * (xCount-1) + \
                dimensions.y * dimensions.x * (zCount-1) + \
                dimensions.x * dimensions.z * (yCount-1)  
                   





class RankMap:
    
    def __init__(self, worldSize, dimensions, split):
        '''
        worldSize is the MPI number of nodes
        dimensions is a Dimensions object, in box count
        '''
        assert (split.x*split.y*split.z == worldSize)

        self.dimensions = dimensions
        
        rMap = {}
        rank = 0
        
        xWidth = dimensions.x / split.x
        yWidth = dimensions.y / split.y
        zWidth = dimensions.z / split.z
        
        # Iterate through the world segments, assigning to ranks
        for x in range(split.x):
            for y in range(split.y):
                for z in range(split.z):
                    (startX, endX) = self._points(x, xWidth)
                    (startY, endY) = self._points(y, yWidth)
                    (startZ, endZ) = self._points(z, zWidth)
                    
                    rMap[rank] = Segment(Coord(startX, startY, startZ),
                                         Coord(endX, endY, endZ))                    
                    rank += 1
                    
        self.rMap = rMap
                    
    def _points(self, segment, width):
        '''
        Returns start value and end value
        '''
        return (segment * width, (segment + 1) * width -1)
    
    def entries(self):
        return self.rMap.items()
    
    def getSegment(self, rank):
        
        assert self.rMap.has_key(rank), "Input rank %d out of bounds (0, %d]" % (rank, len(self.rMap))
        return self.rMap[rank]
    
    def getRank(self, coords):
        '''
        Return MPI rank given coords in the world
        '''

        for (rank, segment) in self.rMap.iteritems():
            if segment.contains(coords):
                return rank
            
        raise Exception("Coord %s not found in any segments of world dimensions %s" % (coords, self.dimensions))