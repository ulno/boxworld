import unittest
from boxworld.RankMap import RankMapGenerator
from boxworld.Coord import Coord
from boxworld.Geometry import Dimensions
from boxworld.RankMap import RankMap
from boxworld.RankMap import Split
from boxworld.RankMap import Segment
from boxworld.Coord import Coord

class RankMapTest(unittest.TestCase):

    def setUp(self):
        self.rankMapGen = RankMapGenerator()

    def testWorldSegementGeneration(self):
        
        
        worldDef = WorldDefinition()
        worldDef.setDimensions(dimensions=Dimensions(100,100,100),
                               timeStart=0,
                               timeDelta=1,
                               timeEnd=100,
                               rankCount=2)
        
        boxDefs = []
        for _ in range(100*100*100):
            boxDefs.append(BoxDefinition(terpLevel=5))
        
        worldDef.setBoxDefinitions(boxDefs)
        
        worldSegment = worldDef.generateWorldSegement(rank=0)
        self.assertEquals(worldSegment.rank, 0)
        self.assertEquals(worldSegment.segment, Segment(Coord(0,0,0), Coord(100, 100, 49)))
    

if __name__ == '__main__':
    unittest.main()
