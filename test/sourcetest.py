# 
# source_test.py
# 
# Author: Steffen M. Noe (steffen.noe@emu.ee)
#
# last revision: 03.03.2011
#

import Source
import numpy as np
import matplotlib.pyplot as plt

# Create a class instance
x = Source.Source(1000,30,2)

# Create a temperature range and an empty array
temps = np.arange(10,51)
a = []

# store all results to the array
for tm in temps:
	a.append( x.guenther(1000,tm) )
	
# plot the result	
plt.plot(temps,a)
plt.xlabel("temperature [C]")
plt.ylabel("emission rate")
plt.show()

