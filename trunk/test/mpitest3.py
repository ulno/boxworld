#! /usr/bin/python
'''
Run as
$mpirun -np X mpitest.py
where X is any integer > 0 

Test a 4 x 4 x 1 world where each box is in a different MPI node

'''
from mpi4py import MPI
from boxworld.MpiChannel import MpiChannel
from boxworld.MpiChannel import MpiChannelFactory
from boxworld.Box import Box
from boxworld.Geometry import Coord
from boxworld.RemoteBox import RemoteBoxFactory
from boxworld.RemoteBox import RemoteManager
from boxworld.WorldSegment import WorldSegmentFactory
import sys
import random




comm = MPI.COMM_WORLD
rank = comm.Get_rank()
worldSize = comm.Get_size()


print "World size = %d" % comm.Get_size()
print "My rank = %d" % rank
file = "../test/testworld.txt"

factory = WorldSegmentFactory(comm.Get_size(), file)
segment = factory.getWorldSegment(rank)

segment.run()

for box in segment.boxes.values():
    print "Done: Box %d, terp_level= %d" % (rank,box.terpene_concentration)

exit(0)



 

