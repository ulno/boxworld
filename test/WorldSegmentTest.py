import unittest
from boxworld.WorldSegement import WorldSegment
from boxworld.WorldSegment import WorldSegmentFactory
from boxworld.Geometry import Dimensions

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

if __name__ == '__main__':
    unittest.main()
