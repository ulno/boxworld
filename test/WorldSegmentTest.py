import unittest
from boxworld.WorldSegement import WorldSegment
from boxworld.WorldSegment import WorldSegmentFactory

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
        
        self.assertEqual(len(factory.sources), 3)
        self.assertEqual(len(factory.sinks), 0)
        self.assertEqual(len(factory.boxes), 0)

if __name__ == '__main__':
    unittest.main()
