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
import random



#light time function
def ltf(time):
    return 1500

# temperature time function
def ttf(time):
    return 30


end_time = 1000
time_delta = 1


box1 = Box((0,0,0),1,ltf,ttf,time_delta,0, end_time, 10)
box2 = Box((1,0,0),1,ltf,ttf,time_delta, 0, end_time, 100)

box1.connect_right(box2)
box2.connect_left(box1)

t1 = box1.run()
t2 = box2.run()

t1.join()
t2.join()

print "Done: Box 1, terp_level= %d" % box1.terpene_concentration
print "Done: Box 2, terp_level= %d" % box2.terpene_concentration


exit(0)



 

