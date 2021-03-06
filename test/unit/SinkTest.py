import unittest
from boxworld.Box import Box
from boxworld.Source import Source
from boxworld.Geometry import Coord
from boxworld.Sink import Sink

class SinkTest(unittest.TestCase):
    
    def testCanonicalSingleStep(self):
         
        sink=Sink(25,15,2,1e-4)
        delta = sink.compute(1,1)
        
        self.assertEqual(delta, -1.2318548715985602)


    def testCanonical(self):
        '''
        Test 1 box with 1 sink for 10 time steps.
        Assert concentration is 1 at the end of the run.
        '''
        
        nair = 101325 * 6.022e23 / (8.314 * (25 + 273.15))
        fnair = nair * 1e-6 * 1e-9
        
        box = Box(position=Coord(0,0,0), 
                  cube_length=1, 
                  light_time_function = lambda t : 1, #always return 1
                temperature_time_function = lambda t : 1, #always return 1 
                timedelta=0.01, 
                initial_time=0, 
                end_time=1.0, 
                initial_terpene=100, 
                sinks=(Sink(25,15,2,1e-4),))
        
        box.run().join()
        
        self.assertEqual(box.terpene_concentration, 1)
        
if __name__ == "__main__":
    unittest.main()
