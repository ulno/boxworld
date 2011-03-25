import unittest
from boxworld.RankMap import RankMapGenerator
from boxworld.Coord import Coord
from boxworld.RankMap import Dimensions
from boxworld.RankMap import RankMap
from boxworld.RankMap import Split
from boxworld.RankMap import Segment
from boxworld.Coord import Coord

class RankMapTest(unittest.TestCase):

    def setUp(self):
        self.rankMapGen = RankMapGenerator()

    def testIdealSplit(self):
        
        split = self.rankMapGen._idealSplit(4, Dimensions(4,4,4))
        self.assertNotEqual(split, None)
        self.assertEqual(split.x, 1)
        self.assertEqual(split.y, 2)
        self.assertEqual(split.z, 2)
        
    def testIdealSplit2(self):
        split = self.rankMapGen._idealSplit(8, Dimensions(4,4,4))
        self.assertNotEqual(split, None)
        self.assertEqual(split.x, 2)
        self.assertEqual(split.y, 2)
        self.assertEqual(split.z, 2)
    
    
    def testCoord(self):
        
        self.assertTrue(Segment(Coord(0,0,0), Coord(0,0,0)).contains(Coord(0,0,0)))
        
    def testCoord2(self):
        
        self.assertFalse(Segment(Coord(0,0,0), Coord(0,0,0)).contains(Coord(1,1,1)))
        
    def testCoord3(self):
        
        self.assertTrue(Segment(Coord(0,0,0), Coord(100,100,100)).contains(Coord(50,50,50)))
    
    def testRankMapBase(self):
        rMap = RankMap(1, Dimensions(1,1,1), Split(1,1,1)) 
        
        self.assertEquals(len(rMap.entries()), 1, "Entries are %s" % rMap.entries())
          
        self.assertEqual(rMap.getRank(Coord(0,0,0)), 0) 
        
    def testRankMap2(self):
        rMap = RankMap(1, Dimensions(2,2,2), Split(1,1,1)) 
        
        self.assertEquals(len(rMap.entries()), 1, "Entries are %s" % rMap.entries())
          
        self.assertEqual(rMap.getRank(Coord(0,0,0)), 0) 
        
    def testRankMap3(self):
        rMap = RankMap(2, Dimensions(2,2,2), Split(1,1,2)) # split half along Z axis 
        
        self.assertEquals(len(rMap.entries()), 2, "Entries are %s" % rMap.entries())
          
        self.assertEqual(rMap.getRank(Coord(0,0,0)), 0) 
        self.assertEqual(rMap.getRank(Coord(0,0,1)), 1) 
        self.assertEqual(rMap.getRank(Coord(0,1,0)), 0) 
        self.assertEqual(rMap.getRank(Coord(0,1,1)), 1) 
        self.assertEqual(rMap.getRank(Coord(1,0,0)), 0)
        self.assertEqual(rMap.getRank(Coord(1,0,1)), 1)
        self.assertEqual(rMap.getRank(Coord(1,1,0)), 0)
        self.assertEqual(rMap.getRank(Coord(1,1,1)), 1)
    

if __name__ == '__main__':
    unittest.main()
