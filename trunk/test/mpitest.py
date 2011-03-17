#! /usr/bin/python
'''
Run as
$mpirun -np X mpitest.py
where X is any integer > 0 
'''
from mpi4py import MPI
from boxworld.MpiChannel import MpiChannel

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

print "World size = %d" % comm.Get_size()
print "My rank = %d" % rank

channel = MpiChannel((rank + 1) % 2)
channel.send("foobar")
print channel.receive()

 

