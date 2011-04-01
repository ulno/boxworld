import unittest
from boxworld.WorldSegement import WorldSegment
from boxworld.WorldSegment import WorldSegmentFactory
from boxworld.Geometry import Dimensions
from boxworld.Geometry import Segment
from boxworld.Geometry import Coord


class WorldSegementTest(unittest.TestCase):

    def setUp(self):
        pass

    def testParseFile1(self):
        file = "./testworld.txt"
        factory = WorldSegmentFactory(4, file)
        
        self.assertEqual(factory.worldSize, 4)
        self.assertEqual(factory.fileName, file)
        self.assertEqual(factory.timeStart, 0)
        self.assertEqual(factory.timeEnd, 1000)
        self.assertEqual(factory.timeDelta, 1)
        self.assertEqual(factory.cubeSize, 1)
        self.assertEqual(factory.dimensions, Dimensions(2,2,2))
        self.assertEqual(factory.dimensions.volume(), 8)
        
        self.assertEqual(len(factory.sources), 3)
        self.assertEqual(factory.sources[1].light, 5)
        self.assertEqual(factory.sources[1].temperature, 4)
        self.assertEqual(factory.sources[1].e0, 10)
        
        self.assertEqual(len(factory.sinks), 3)
        #7,4,5,1,4
        
        self.assertEqual(factory.sinks[1].terpene_concentration,7)
        self.assertEqual(factory.sinks[1].temperature, 277.15)
        self.assertEqual(factory.sinks[1].ozone, 5)
        self.assertEqual(factory.sinks[1].nox,1)
        self.assertEqual(factory.sinks[1].oh, 4)
        
        self.assertEqual(len(factory.lightFuncs), 2)
        self.assertEqual(len(factory.tempFuncs), 2)
        
        self.assertEqual(len(factory.boxes), 8)
        
        for rank in range(4):
            segment = factory.getWorldSegment(0)
            self.assertNotEqual(segment, None)
            self.assertEqual(len(segment.boxes), 2)
            
            for box in segment.boxes.values():
                self.assertHasAllNeighbors(box, Dimensions(2,2,2))

    def assertHasAllNeighbors(self, box, dimensions):
        '''
        Given a box and world dimensions, assert that box has all required neighbors connected to it.
        '''
        
        
        segment = Segment(Coord(0,0,0), Coord(dimensions.x-1,dimensions.y-1, dimensions.z-1))
        for p in box.position.surroundingCoords():
            if segment.contains(p):
                self.assertTrue(box.neighbors.has_key(p) and box.neighbors[p] != None, 
                                "Box at %s does not have neighbor %s" % (box.position, p))
            
if __name__ == '__main__':
    unittest.main()
