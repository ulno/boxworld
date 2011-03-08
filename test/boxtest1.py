'''
boxtest1.py

Test module to create some boxes and connect them together
Here we need to define some transport logic as well, easy approach is to pass some percent over
if there is a difference between the two boxes

Created on 7.3.2011

@author: steffen
'''

import numpy as np
import boxworld.Box as box
import boxworld.Source as sc
import boxworld.Chemical_Sink as cs
import boxworld.Transport as tr
import boxworld.Inbox as ib
import random

'''
create a set of boxes

The first one will hold a source, and a sink, the others should hold just sink terms now.
The position is now chosen to be easy and the first box is centered at [0,0,0]
There are no boxes in the "corners" yet for simplicity
'''

end_time = 100

#light time function
def ltf(time):
    return 1500

# temperature time function
def ttf(time):
    return 30

#max_x = 2
#max_y = 0
#max_z = 2




world = {} # Coordinate tuple => box map

# Create one box and all its neighbors
# (x, y, z)
points = ((0,0,0), (1,0,0), (-1,0,0), (0,-1,0), (0,1,0), (0,0,1), (0,0,-1))

for p in points:
    world[p] = box.Box(p,1,ltf,ttf,10,0, end_time, random.randint(0,10))

# Connect all the boxes together
# Use 'right-hand-rule' for orientation
for (point, box) in world.iteritems():
    up = (point[0], point[1] + 1, point[2])
    down = (point[0], point[1] - 1, point[2])
    left = (point[0] - 1, point[1], point[2])
    right = (point[0] + 1, point[1], point[2])
    front = (point[0], point[1], point[2] - 1)
    back = (point[0], point[1], point[2] + 1)
    
    if world.has_key(up):
        box.connect_up(world[up])
        
    if world.has_key(down):
        box.connect_down(world[down])
        
    if world.has_key(left):
        box.connect_left(world[left])
        
    if world.has_key(right):
        box.connect_right(world[right])
        
    if world.has_key(front):
        box.connect_front(world[front])
        
    if world.has_key(back):
        box.connect_back(world[back])


# Finally, we run the simulation.
threads = []
for box in world.values():
    threads.append(box.run())
    
for t in threads:
    t.join()

#if __name__ == '__main__':
#    pass