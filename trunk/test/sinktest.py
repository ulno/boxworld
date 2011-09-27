'''
Testing the sink behaviour

Created on 27.09.2011

@author: steffen
'''

import Sink as cs
import numpy as np
import matplotlib.pyplot as plt

# scaling to convert ppbv to molecules per cube meter (m3)
#
nair = 101325 * 6.022e23 / (8.314 * (25 + 273.15))
fnair = nair * 1e-6 * 1e-9

# x = cs.Sink(5.0e11,25,15*fnair,2*fnair,1e-4*fnair)
x = cs.Sink(5.0,25,15,2,1e-4)

time = np.arange(100)
deltaTime = 0.1
y = [x.terpene_concentration]
print y

for t in time:
    h = x.terpene_concentration + x.compute(deltaTime)
    x.terpene_concentration = h
    y.append(h)
    
# print y
plt.plot(y)
plt.xlabel("time")
plt.ylabel("concentration rate")
plt.show()
