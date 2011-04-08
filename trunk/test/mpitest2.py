#! /usr/bin/python
'''
Run as
$mpirun -np X mpitest.py
where X is any integer > 0 
'''
from mpi4py import MPI
from boxworld.MpiChannel import MpiChannel
from boxworld.MpiChannel import MpiChannelFactory
from boxworld.Box import Box
from boxworld.RemoteBox import RemoteBoxFactory
from boxworld.RemoteBox import RemoteManager
from boxworld.Geometry import Coord
import random



#light time function
def ltf(time):
    return 1500

# temperature time function
def ttf(time):
    return 30

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

print "World size = %d" % comm.Get_size()
print "My rank = %d" % rank

class TestRankMap:
    
    def getRank(self, coords):
        if coords == Coord(0,0,0):
            return 0
        elif coords == Coord(1,0,0):
            return 1
        else:
            raise Exception("Why were you looking for coords: %s" % str(coords))

remoteChannelFactory = MpiChannelFactory(TestRankMap())
remoteManager = RemoteManager(remoteChannelFactory) 
rbFactory = RemoteBoxFactory(remoteChannelFactory, remoteManager)

end_time = 1000
time_delta = 1

if rank == 0:
    box = Box(Coord(0,0,0),1,ltf,ttf,time_delta,0, end_time, 10)
    rBox = rbFactory.getBox(Coord(1,0,0))
    box.connect_right(rBox)
    rBox.connect(box)
else:
    box = Box(Coord(1,0,0),1,ltf,ttf,time_delta, 0, end_time, 100)
    rBox = rbFactory.getBox(Coord(0,0,0))
    box.connect_left(rBox)
    rBox.connect(box)


t = box.run()
rBox.run()

remoteManager.run()

t.join()
remoteManager.stop()
print "Done: Box %d, terp_level= %d" % (rank,box.terpene_concentration)

exit(0)



 

