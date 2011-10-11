import unittest
from boxworld.Box import Box
from boxworld.Source import Source
from boxworld.Geometry import Coord

class SourceTest(unittest.TestCase):
    
    def testCanonical(self):
        '''
        Test 1 box with 1 source for 10 time steps.
        Assert concentration is 1 at the end of the run.
        '''
        
        box = Box(position=Coord(0,0,0), 
                  cube_length=1, 
                  light_time_function = lambda t : 1, #always return 1
                temperature_time_function = lambda t : 1, #always return 1 
                timedelta=1, 
                initial_time=0, 
                end_time=10, 
                initial_terpene=1, 
                sources=(Source(baseEmission=1),), 
                sinks=())
        
        box.run().join()
        
        self.assertEqual(box.terpene_concentration, 15.730507560710043)
    
    
if __name__ == "__main__":
    unittest.main()
